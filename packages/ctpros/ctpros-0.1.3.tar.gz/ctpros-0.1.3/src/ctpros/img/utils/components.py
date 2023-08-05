import numpy as np
import scipy as sp
import os, copy, itertools


class AffineTensor(np.ndarray):
    """
    Affine tensors describe a linear mapping from one space to another.

    For images, the mapping describes:
     - matrix index space --> physical coordinate space
       Ex: [0,0,0]px --> [offset_x,offset_y,offset_z] um
    """

    def __new__(thisclass, *args, **kwargs):
        if type(args[0]) == int:
            pdim = args[0]
        else:
            pdim = 1
        instance = super().__new__(thisclass, (pdim + 1, pdim + 1))
        instance[:] = np.eye(pdim + 1)
        if type(args[0]) == str:
            if os.path.isfile(args[0]):
                if os.path.splitext(args[0])[-1].lower() == ".tfm":
                    instance.fileloc = (
                        os.path.dirname(os.path.abspath(args[0])) + os.path.sep
                    )
                    instance.filename = os.path.basename(args[0])
                    instance.load()
                else:
                    raise Exception(
                        "Expected filetype *.tfm, received *{}".format(
                            os.path.splitext(args[0])[-1].lower()
                        )
                    )
            else:
                raise Exception("Could not find file {}".format(args[0]))

        return instance

    def __init__(self, pdim=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pdim = self.shape[0] - 1

    def __array_finalize__(self, parent):
        self.pdim = getattr(parent, "pdim", 3)

    def _snap(self, eps_angle=1e-3, eps_stretch=1e-8):
        """Snaps the tensor to 0 rotation if rotations are extremely small"""
        angles = self.rotate()
        snapflags = np.array(
            [abs(angle) < eps_angle and angle != 0 for angle in angles]
        )
        if np.any(snapflags):
            snapped = np.array(
                [angle if abs(angle) >= eps_angle else 0 for angle in angles]
            )
            _, V, T = self.decomposition("RVT")
            V[V - np.eye(V.pdim + 1) < eps_stretch] = np.eye(V.pdim + 1)[
                V - np.eye(V.pdim + 1) < eps_stretch
            ]
            self[:] = (
                AffineTensor(self.pdim).affine(T).affine(V).rotate(*snapped, snap=False)
            )

    def decomposition(self, labels):
        """
        Labels in affine multiplication order. Labels define components to output
        and the order in which they are computed.

        V or stretch is the Left Stretch Tensor or the stretch in the un-decomposed coordinate system.
        To acquire u, the Right Stretch Tensor, pass V after R
        Example w/ Left Stretch:
        S,V,R,T,A = affine.decomposition("SVRTA")
            S = Scaling relative to new coordinate system
            V = Stretch between old and new coordinate system axes
            R = Rotation "   "
            T = Translation "   "
            A = Affine remainder of decomposition (in this case I)

        A common usage for this is to acquire the scaling or stretch
        of the elements in the original coordinate system:
            _, S = affine.decomposition("RS")
            original_scaling = S.scale()
        """
        affine = self.copy()  # matrix being modified
        components = []
        for label in labels:
            base = AffineTensor(affine.pdim)  # container for composite step
            if label.lower() == "r":
                base.rotate(*affine.rotate(snap=False), snap=False)
            elif label.lower() == "t":
                base.translate(*affine.translate())
            elif label.lower() == "s":
                base.scale(*affine.scale())
            elif label.lower() == "a":
                base.affine(affine)
            elif label.lower() == "v":
                base.stretch(*affine.stretch())
            else:
                raise Exception(
                    "Decomposition labels must be of the following:\nR: Rotation\nT: Translation\nS: Scaling\nA: Affine (remainder)"
                )
            affine.affine(base.copy().inv())
            components += [base]
        return components

    def load(self):
        """
        Loads n filename into the affine tensor, reshaping as necessary.

        """
        with open(self.fileloc + self.filename, "rb") as f:
            data = np.fromfile(f, np.float64)

        i = 0
        while 1:
            if len(data) == i * (i + 1):
                self.pdim = i
                break
            else:
                i += 1

        self.resize((self.pdim + 1, self.pdim + 1), refcheck=False)
        self[: self.pdim, : self.pdim + 1].ravel()[:] = data
        self.ravel()[-1] = 1
        return self

    def save(self):  # pragma: no cover
        self.saveas(self.fileloc + self.filename)

    def saveas(self, filename):
        """
        Saves the affine tensor to a file defined by the input filename.

        """
        self.fileloc = os.path.abspath(os.path.dirname(filename)) + os.path.sep
        self.filename = os.path.basename(filename)
        with open(self.fileloc + self.filename, "wb") as f:
            self[: self.pdim, : self.pdim + 1].tofile(f)

    def copy(self):
        return copy.deepcopy(self)

    def inv(self):
        self[:] = np.linalg.inv(self)
        return self

    def root(self):
        self[:] = sp.linalg.sqrtm(self)
        return self

    def flip(self, *axes, physshape):
        for axis in axes:
            self[axis, : self.pdim] = -self[axis, : self.pdim]
            self[axis, -1] += physshape[axis]
            self[axis, -1] -= self.scale()[axis]
        return self

    def swap(self, m, n):
        """
        Performs an axis swapping operation.
        """
        affine = AffineTensor(self.pdim)
        affine[m, m] = 0
        affine[n, n] = 0
        affine[m, n] = 1
        affine[n, m] = 1
        return self.affine(affine)

    def scale(self, *scales):
        if len(scales) == 0:
            return self._get_scaling()
        elif len(scales) == 1:
            scales = np.array([*([scales[0]] * self.pdim), 1]).astype(np.float64)
        else:
            scales = np.array([*scales, 1]).astype(np.float64)
        affine = np.eye(self.pdim + 1)
        affine *= scales
        self[:] = np.dot(affine, self)
        return self

    def _get_scaling(self):
        return np.linalg.norm(self[: self.pdim, : self.pdim], 2, 1)

    def translate(self, *translates):
        translates = np.array(translates, dtype=np.float64).ravel()
        if not translates.size:
            return self._get_translation()
        if translates.size != self.pdim:
            raise Exception
        self.ravel()[self._get_trans_inds()] += translates.ravel()
        return self

    def _get_translation(self):
        translation = np.empty(self.pdim, dtype=np.float64)
        translation[:] = self.ravel()[self._get_trans_inds()]
        return translation

    def _get_trans_inds(self):
        return np.arange(self.pdim, (self.pdim + 1) ** 2, self.pdim + 1)[:-1]

    def rotate(self, *angles, snap=True):
        """
        Angles are related by axis pairs generated via itertools.
        Ex:
            R = AffineTensor(3).rotate(a,b,c)
            (0,1) --> a (rotation from 0 towards 1)
            (0,2) --> b
            (1,2) --> c

        """
        if not angles:
            return self._get_rotation()
        expectedangles = sum(range(self.pdim))
        if len(angles) != expectedangles:
            raise Exception(
                "Expected {} angles for {}-dimensional Affine Tensor, but got {}.".format(
                    expectedangles, self.pdim, len(angles)
                )
            )

        result = np.eye(self.pdim + 1)
        for (x, y), angle in zip(itertools.combinations(range(self.pdim), 2), angles):
            R = np.eye(self.pdim + 1)
            R[[x, x, y, y], [x, y, x, y]] = (
                np.cos(angle),
                -np.sin(angle),
                np.sin(angle),
                np.cos(angle),
            )
            result[:] = np.dot(result, R)

        self[:] = np.dot(result, self)
        if snap:
            self._snap()
        return self

    def _get_rotation(self):
        """
        Returns the angles associated to the left rotation matrix
        via polar decomposition where F is self:

        F = RU
        F.T*F = U^2
        F = R*root(F.T*F)
        R = F*root(F.T*F)^-1

        Angles are extracted as follows:
            For rotation from axis x to y:
            1. Extract rotation matrix (R) from affine tensor.
            2. Multiply unit vector along x (r = R*e_x)
            3. Project r onto 2D plane x-y (e_x --> p_x, r --> p)
            4. angle = arctan2(cross(p_x,p),dot(p_x,p))

        """

        if self.pdim == 1:
            raise Exception(
                "Attempted to rotate a 1D affine tensor, where rotation does not exist in 1D."
            )
        else:
            angles = []
            F = self[: self.pdim, : self.pdim]
            R = AffineTensor(self.pdim)
            R[: self.pdim, : self.pdim] = F.copy().affine(F.T).root().inv().affine(F)
            for i, (x, y) in enumerate(itertools.combinations(range(self.pdim), 2)):
                e_x = [[0] for _ in range(self.pdim)]
                e_x[x][0] = 1
                r = np.dot(R[:-1, :-1], e_x)

                p_x = [0] * 2
                p_x[0] = 1
                p = [r[x][0], r[y][0]]
                angle = np.arctan2(np.cross(p_x, p), np.dot(p_x, p))
                angles += [angle]

                unrotate_angles = [0] * sum(range(self.pdim))
                unrotate_angles[i] = -angle
                R.rotate(*unrotate_angles, snap=False)

            return np.array([angle if angle != 0.0 else 0.0 for angle in angles])

    def stretch(self, *stretches):
        """
        Stretches are scaling relations between all axes in a coordinate system.
        This will pass the

        For a coordinate system F:
        F = VR = RU

        R is an orthogonal tensor and V/U are positive definite symmetric tensors.

        F*F^T = V^2
        V = sqrt(F*F^T)

        Stretches are defined in the orter of itertools combinations with replacement:

        affine.stretch(a,b,c) # 2D tensor --> 3 stretches
        a = stretch between old axis 0 and new axis 0
        b = stretch between old axis 0 and new axis 1 (by symmetry, the inverse relation is identical)
        c = stretch between old axis 1 and new axis 1
        """
        if not stretches:
            return self._get_stretch()
        expectedstretches = sum(range(self.pdim + 1))
        if len(stretches) != expectedstretches:
            raise Exception(
                "Expected {} stretches for {}-dimensional Affine Tensor, but got {}.".format(
                    expectedstretches, self.pdim, len(stretches)
                )
            )
        else:
            V = np.dot(self, self.T).root()
            self.affine(V.inv())

            indices = np.array(
                list(itertools.combinations_with_replacement(range(self.pdim), 2))
            )
            V[indices[:, 0], indices[:, 1]] = stretches
            stretches = [
                stretch
                for i, stretch in enumerate(stretches)
                if indices[i][0] != indices[i][1]
            ]
            indices = np.array([(y, x) for (x, y) in indices if x != y])
            V[indices[:, 0], indices[:, 1]] = stretches
            np.linalg.cholesky(V)  # asserts positive definite matrix
            self.affine(V)
            return self

    def _get_stretch(self):
        V = np.dot(
            self[: self.pdim, : self.pdim], self[: self.pdim, : self.pdim].T
        ).root()
        indices = np.array(
            list(itertools.combinations_with_replacement(range(self.pdim), 2))
        )
        return V[indices[:, 0], indices[:, 1]]

    def affine(self, myaffine):
        self[:] = np.dot(myaffine, self)
        return self

    def dot(self, vector):
        if not issubclass(type(vector), np.ndarray):
            vector = np.array(vector)
        if vector.shape[0] + 1 == self.shape[-1]:
            if vector.ndim == 1:
                return np.dot(self.view(np.ndarray), np.array([*vector, 1]))[:-1]
            else:
                padsize = vector.shape[1]
            return np.dot(self.view(np.ndarray), np.array([*vector, [1] * padsize]))[
                :-1
            ]
        else:
            return np.dot(self.view(np.ndarray), vector)

    def voi(self, myvoi):
        self.translate(-myvoi.pos)
        self.scale(*(1 / myvoi.elsize))
        return self, myvoi.shape.astype(int)

    def align(self, affine):
        """
        Alignment of two coordinate systems refers to the application of identical affine transformations over the base
        scale factor into physical coordinates.

        If affine A = RTS where "R","T","S" are composites of rotation, translation, and scaling, all but scaling are applied to the original affine

        affine.align(aligner) --> A.align(B) --> RaTaSa.align(RbTbSb) = RbTbSa

        """
        _, _, S = self.decomposition("RTS")
        R, T, _ = affine.decomposition("RTS")
        self[:] = S.affine(T).affine(R)
        return self


class VOI:
    """Volume Of Interest. Descriptor of volume grid of interest to be sampled.

    Has the following attributes of interest:
    - pos (um) = offset corner where sampling begins relative to physical space
    - shape (pix) = number of samples to take (pixels to draw)
    - elsize (um) = density for samples to be taken relative to physical space
    """

    def __repr__(self):
        return "position:\n{}\nshape:\n{}\nelsize:\n{}".format(
            self.pos, self.shape, self.elsize
        )

    def __init__(self, filename=None, *, pos=None, shape=None, elsize=None):
        """
        Instantiates the dimensionality of the VOI

        """
        if pos is None:
            self.pos = np.zeros((3, 1))
        else:
            self.pos = np.array(pos, dtype=np.float64).reshape((-1, 1))

        if shape is None:
            self.shape = np.zeros(3, dtype=np.uint64)
        else:
            self.shape = np.array(shape, dtype=np.uint64).reshape(-1)

        if elsize is None:
            self.elsize = np.ones(3)
        else:
            self.elsize = np.array(elsize, dtype=np.float64).reshape(-1)

        if filename is None:
            self.filename = filename
            self.fileloc = "." + os.path.sep
        elif type(filename) is str:
            if os.path.isfile(filename):
                if os.path.splitext(filename)[-1].lower() == ".voi":
                    self.filename = os.path.basename(filename)
                    self.fileloc = (
                        os.path.abspath(os.path.dirname(filename)) + os.path.sep
                    )
                    self.load()
                else:
                    raise Exception("VOI attempted to read non *.voi filetype.")
            else:
                raise Exception("VOI file {} not found.".format(filename))
        else:
            raise Exception("Unknown input when initializing class VOI.")

    def load(self):
        """
        Loads a binary file with VOI position and shape defined as doubles.

        """
        with open(self.fileloc + self.filename, "rb") as f:
            dtypes = (np.float64, np.uint64, np.float64)
            shapes = ((3, 1), (3), (3))
            self.pos, self.shape, self.elsize = [
                np.fromfile(f, dtype=dtype, count=3).reshape(shape)
                for dtype, shape in zip(dtypes, shapes)
            ]

        return self

    def saveas(self, filename):
        """
        Saves a binary file with VOI position and shape defined as doubles.

        """
        fileloc = os.path.abspath(os.path.dirname(filename)) + os.path.sep
        filename = os.path.basename(filename)
        if not os.path.isdir(fileloc):
            raise Exception(
                "Attempted to write file {} to path {} but path was not found.".format(
                    filename, fileloc
                )
            )
        else:
            self.filename = filename
            self.fileloc = fileloc
            with open(fileloc + filename, "wb") as f:
                self.pos.tofile(f)
                self.shape.tofile(f)
                self.elsize.tofile(f)

    def copy(self):
        return copy.deepcopy(self)
