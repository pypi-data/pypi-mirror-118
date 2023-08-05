import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import threading, time, math, os
import numpy as np

from ... import img
from .progressbar import LinkedIterator
from . import tools


def cache_event(**kwargs):
    """Returns a decorator which establishes a 'cache' in self."""

    def mk_cache(method):
        """The decorator."""

        def decorated_method(self, event):
            """The decorated method."""
            kwargs["mod"] = kwargs.pop("mod", None)
            self.cache = {"event": event, **kwargs}
            method(self, event)

        return decorated_method

    return mk_cache


class FloatRangeEntry(ttk.Spinbox):
    vartype = tk.DoubleVar

    def __init__(
        self,
        master,
        *args,
        minval,
        maxval,
        precision=1,
        validate="all",
        var=None,
        **kwargs,
    ):
        """
        Generates helper functions to alter the entry input when an input is deemed inappropriate.
        Default validation check is set to "all".

        """
        self.precision = precision
        if var is None:
            self.var = type(self).vartype()
            self.var.set(minval)
        else:
            self.var = var

        self.minval = minval
        self.maxval = maxval

        validatecommand = (
            master.register(self.validatefunction),
            "%s",
            "%P",
            "%S",
            "%i",
            "%V",
            "%d",
        )
        invalidcommand = (
            master.register(self.invalidfunction),
            "%s",
            "%P",
            "%S",
            "%i",
            "%V",
            "%d",
        )

        super().__init__(
            master,
            width=5,
            validate="all",
            from_=minval,
            to=maxval,
            validatecommand=validatecommand,
            invalidcommand=invalidcommand,
            justify=tk.LEFT,
            textvariable=var,
            *args,
            **kwargs,
        )
        try:
            self.set(self.var.get())
        except:
            pass

            self.config(state="enabled")

    def set(self, val):
        self.invalidfunction(
            prior="",
            current=str(val),
            alter=str(val),
            index="0",
            how="focusout",
            type="1",
        )

    def invalidfunction(self, prior, current, alter, index, how, type):
        """
        On focusout:
            If empty, set to minval
            Remove leading and trailing zeros

        On key:
            If not numeric: do not insert
            If beyond abs bound: set to abs bound
            If beginning with 0's, remove leading 0's up to decimal
            If begins with ".", add 0 to front
            if

        """
        if how == "focusin":  # pragma: no cover  # just select all text
            self.selection_range(0, tk.END)
            return None
        elif how == "focusout":  # apply all final touches
            current = self._set_minval_if_empty(current)
            current = self._remove_leading_zeros(current)
            current, index = self._add_leading_zero_if_nowhole(current, index)
            current = self._truncate_to_precision(current)
            current = self._remove_trailing_zeros_decimal(current)
            current = self._cap_realval(current)
            super().set(current)
            self.var.set(current)
            if self.get() != current:
                super().set(current)
        elif how == "key":  # apply minimal touches
            current = self._replace_if_prior_is_zero_and_added(
                alter, prior, current, type
            )
            current = self._flip_sign_if_minus(alter, prior, current)
            current, index = self._add_leading_zero_if_nowhole(current, index)
            if self._ignore_input(alter, current):
                return
            current = self._cap_absval(current)

            super().set(current)
            self._set_index(index, type, alter)
        else:
            raise Exception(f"Unknown call type to {type(self).__name__}")

    def set_min(self, newmin, *, overwrite=True):
        self.minval = newmin
        self.configure(from_=newmin)
        try:
            if self.var.get() < newmin and overwrite:
                self.set(newmin)
        except:
            pass

    def set_max(self, newmax, *, overwrite=True):
        self.maxval = newmax
        self.configure(to=newmax)
        try:
            if self.var.get() > newmax and overwrite:
                self.set(newmax)
        except:
            pass

    def validatefunction(
        self, prior, current, alter, index, how, type
    ):  # pragma: no cover
        """ """
        return False

    def _cap_absval(self, current):
        if current in ["-", ".", ""]:
            return current
        val = float(current)
        maxabsval = max(abs(self.minval), abs(self.maxval))
        if abs(val) > maxabsval:
            val = maxabsval
            return str(val)
        else:
            return current

    def _cap_realval(self, current):
        val = float(current)
        if val > self.maxval:
            return str(self.maxval)
        elif val < self.minval:
            return str(self.minval)
        else:
            return current

    def _ignore_input(self, alter, current):
        if current in ["-", ".", ""]:
            return False

        try:
            float(current)
        except:
            return True

        return alter == " " or (
            "." in current and len(current.split(".")[1]) > self.precision
        )

    def _set_index(self, index, type, alter):
        if type == "1":
            fixedindex = int(index) + len(alter)
        else:
            fixedindex = int(index) - len(alter) + 1

        self.selection_range(fixedindex, fixedindex)
        self.icursor(fixedindex)
        return fixedindex

    def _flip_sign_if_minus(self, alter, prior, current):
        if alter == "-":
            if prior == "0" or not prior:
                current = "-"
            elif prior[0] == "-":
                current = prior[1:]
                if not current:
                    current = "0"
            else:
                current = "-" + prior
        return current

    def _remove_trailing_zeros_decimal(self, current):
        if "." not in current:
            return current
        whole, decimal = current.split(".")
        while decimal and decimal[-1] == "0":
            decimal = decimal[:-1]
        if not decimal:
            return whole
        else:
            return f"{whole}.{decimal}"

    def _set_minval_if_empty(self, current):
        if not current:
            current = str(self.minval)
        return current

    def _remove_leading_zeros(self, current, allowed=1):
        while current[0] == "0" and len(current) > allowed:
            current = current[1:]
        return current

    def _replace_if_prior_is_zero_and_added(self, alter, prior, current, type):
        if prior in ["0", "-0"] and type == "1":
            return alter
        else:
            return current

    def _truncate_to_precision(self, current):
        if "." in current:
            whole, decimal = current.split(".")
            return f"{whole}.{decimal[: self.precision]}"
        else:
            return current

    def _add_leading_zero_if_nowhole(self, current, index):
        if "." in current:
            whole, decimal = current.split(".")
            if not whole:
                whole = "0"
                return f"{whole}.{decimal}", str(int(index) + 1)
            else:
                return current, index
        else:
            return current, index


class IntRangeEntry(FloatRangeEntry):
    vartype = tk.IntVar

    def invalidfunction(self, prior, current, alter, index, how, type):
        if "." in alter:
            return
        super().invalidfunction(prior, current, alter, index, how, type)


class IntScale(ttk.Scale):
    def __init__(self, *args, entry, **kwargs):
        self.var = kwargs.pop("variable", entry.var)
        self.entry = entry
        super().__init__(
            *args,
            from_=self.entry.minval,
            to=self.entry.maxval,
            command=self.set,
            variable=self.var,
            **kwargs,
        )

    def set(self, val):
        self.entry.set(str(round(float(val))))


class OptionMenu(ttk.OptionMenu):
    def get_options(self):
        menu = self["menu"]
        size = menu.index("end") + 1
        return [menu.entrycget(index, "label") for index in range(size)]


def thread(label=None):  # pragma: no cover
    """
    Decorates a method to be threaded and show progress in the GUI.

    """

    def intermediate(func):
        def wrapper(self, *args, **kwargs):
            progressbar = self.master.progressbar
            progressbar["mode"] = "indeterminate"
            progressbar.start()
            mythread = threading.Thread(target=func, args=(self, *args), kwargs=kwargs)
            mythread.start()
            while mythread.isAlive():
                progressbar.step()
                self.master.update_idletasks()
                time.sleep(0.0075)
            progressbar.stop()
            progressbar["mode"] = "determinate"
            progressbar.progress.set(0)
            return None

        return wrapper

    return intermediate


class BackEnd_MixIn:
    def mainloop(self, *args, **kwargs):  # pragma: no cover
        self.flag_render.set(True)
        super().mainloop(*args, **kwargs)

    def __init__(self, *imgs, withdraw=False, verbosity=2):
        """
        Defines the initialization behavior defined below:

        Parameters:
            - imgs = a set of NDArrays


        """
        super().__init__()
        if withdraw:  # pragma: no cover
            self.withdraw()

        self.resizable(height=False, width=False)
        self.geometry("%dx%d+%d+%d" % (500, 0, 0, 0))
        self.geometry("")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.lift()
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.title("Computed Tomography Processing & Registration - Open-Sourced")
        self.__init_vars()
        self.imgs = []
        self.front(verbosity)
        self.__init_listeners()
        self.__init_binds()
        self.add_imgs(*imgs)

    def add_imgs(self, *imgs):
        imgs = [
            img.ImgTemplate(newimg) if type(newimg) is str else newimg
            for newimg in imgs
        ]
        self.imgs.extend(imgs)
        self.fill_selection(*imgs)
        self.refresh()

    def __init_vars(self):
        self.selected_imgnames = [
            tk.StringVar(),
            tk.StringVar(),
        ]
        self.flag_crosshair = tk.BooleanVar()
        self.flag_voi = tk.BooleanVar()
        self.flag_zoom = tk.BooleanVar()
        self.flag_render = tk.BooleanVar()
        self.flag_redblue = tk.BooleanVar()
        self.samplerate = tk.DoubleVar()  # pixel/micron
        self.sampleshape = [tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()]
        self.pos = [tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()]  # img px
        self.voi = {
            "pos": [
                tk.DoubleVar(),
                tk.DoubleVar(),
                tk.DoubleVar(),
            ],  # img px
            "shape": [tk.IntVar(), tk.IntVar(), tk.IntVar()],  # voxels
            "elsize": [
                tk.DoubleVar(),
                tk.DoubleVar(),
                tk.DoubleVar(),
            ],  # microns/image px
        }
        self.imgs = []
        self.loc = os.getcwd()

        self.default_vars()

    def default_vars(self):
        [imgname.set("None") for imgname in self.selected_imgnames]
        for var in self.pos:
            var.set("")
        for _, prop in self.voi.items():
            for var in prop:
                var.set("")
        self.flag_crosshair.set(True)
        self.flag_voi.set(False)
        self.flag_zoom.set(False)
        self.flag_redblue.set(False)
        self.samplerate.set(1)

    def __init_listeners(self):
        self.traced_vars = [
            *self.selected_imgnames,
            *self.pos,
            *self.voi["pos"],
            *self.voi["shape"],
            *self.voi["elsize"],
            self.flag_crosshair,
            self.flag_voi,
            self.flag_zoom,
            self.flag_render,
        ]
        for i, p in enumerate(self.pos):
            p.trace("w", (lambda i: lambda *args, **kwargs: self.push_pos(i))(i))
        for i, voip in enumerate(self.voi["pos"]):
            voip.trace(
                "w", (lambda i: lambda *args, **kwargs: self.update_voi(i, "pos"))(i)
            )
        for i, vois in enumerate(self.voi["shape"]):
            vois.trace(
                "w", (lambda i: lambda *args, **kwargs: self.update_voi(i, "shape"))(i)
            )
        for i, voie in enumerate(self.voi["elsize"]):
            voie.trace(
                "w", (lambda i: lambda *args, **kwargs: self.update_voi(i, "elsize"))(i)
            )
        self.flag_crosshair.trace("w", (self.draw_crosshairs))
        self.flag_voi.trace("w", (self.draw_vois))
        self.flag_zoom.trace("w", lambda *args: self.zoomresponse())
        self.flag_render.trace("w", lambda *args: self.imgframe.refresh())
        self.flag_redblue.trace("w", lambda *args: self.imgframe.refresh())

    def zoomresponse(self):
        self.default_samplerate()
        self.imgframe.refresh()

    def remove_traces(self):
        for var in self.traced_vars:
            for trace in var.trace_vinfo():
                var.trace_vdelete(*trace)

    def __init_binds(self):
        self.bind("<Shift-V>", self.toggle_voi)
        self.bind("<Shift-C>", self.toggle_crosshairs)
        self.bind("<Shift-Z>", self.toggle_zoom)

    def draw_crosshairs(self, *args):
        self.traframe.canvas.draw_crosshairs()
        self.corframe.canvas.draw_crosshairs()
        self.sagframe.canvas.draw_crosshairs()

    def toggle_voi(self, event):
        self.flag_voi.set(not self.flag_voi.get())

    def toggle_crosshairs(self, event):
        self.flag_crosshair.set(not self.flag_crosshair.get())

    def toggle_zoom(self, *args):
        self.flag_zoom.set(not self.flag_zoom.get())
        self.imgframe.refresh()

    def update_voi(self, ind, field=None):
        try:
            self.voi[field][ind].get()
            if field == "pos":
                update = self.push_voipos(ind)
            elif field == "shape":
                update = self.push_voishape(ind)
            elif field == "elsize":
                update = self.push_voielsize(ind)
            if update:
                self.pull_limits()
            if self.flag_zoom.get():
                self.refresh()
            else:
                self.draw_vois()
        except:
            pass

    def draw_vois(self, *args, **kwargs):
        imgframes = [self.traframe, self.corframe, self.sagframe]
        for frame in imgframes:
            frame.canvas.draw_voi()

    def new_selection(self, ind):
        self.imgselect.update_selection(ind)

    def refresh(self):
        self.loadunload_imgs()
        self.check_enable()
        self.pull_allinfo()
        self.default_samplerate()
        self.push_allinfo()

        self.imgselect.refresh()
        self.imgframe.refresh()
        self.menu.refresh()

    def get_selected_imgnames(self):
        return [var.get() for var in self.selected_imgnames]

    def get_options(self):
        return ["None", *[myimg.filename for myimg in self.imgs]]

    def get_selected_img_inds(self):
        options = self.get_options()
        return [options.index(var.get()) for var in self.selected_imgnames]

    def get_selected_imgs(self):
        """
        Returns selected images from dropdown menus.

        """
        return [
            self.imgs[i - 1]
            for i in self.get_selected_img_inds()
            if self.get_options()[i] != "None"
        ]

    def fill_selection(self, *newimgs):
        """
        Updates values with a refresh, then fills in new selection of images.

        """
        imgnames = [myimg.filename for myimg in newimgs]
        for var in self.selected_imgnames:
            if not imgnames:
                break
            if var.get() == "None":
                var.set(imgnames[0])
                self.imgselect.mkcache()
                imgnames = imgnames[1:]

    def loadunload_imgs(self):
        """
        Loads images seleced via main frame dropdown menus and unloads those not.

        """
        [
            myimg.clear()
            for myimg in self.imgs
            if myimg.filename not in self.get_selected_imgnames() and myimg.nbytes != 0
        ]
        [myimg.load() for myimg in self.get_selected_imgs() if myimg.nbytes == 0]

    def pull_allinfo(self):
        self.remove_traces()
        self.pull_limits()
        self.pull_position()
        self.pull_voi()
        self.__init_listeners()

    def pull_voi(self):
        if self.get_selected_imgs():
            self.set_voi(self.get_selected_imgs()[0].voi)

    def pull_position(self):
        if self.get_selected_imgs():
            primaryimg = self.get_selected_imgs()[0]
            self.set_pos(primaryimg.position.ravel() / primaryimg.affine.scale())

    def pull_limits(self):
        loadedimgs = [myimg for myimg in self.get_selected_imgs() if myimg is not None]
        if loadedimgs:
            self.maxpos = (
                img.utils.script.maxshape(*loadedimgs) / loadedimgs[0].affine.scale()
            )
            self.maxelsize = img.utils.script.maxshape(*loadedimgs)
        else:
            self.maxpos = img.utils.script.maxshape() + 1
            self.maxelsize = img.utils.script.maxshape() + 1

        for (
            posentry,
            scale,
            voiposentry,
            voishapeentry,
            voielsizeentry,
            pos,
            elsize,
        ) in zip(
            self.imgpos.entries,
            self.imgpos.scales,
            self.voiinfo.posentries,
            self.voiinfo.shapeentries,
            self.voiinfo.elsizeentries,
            self.maxpos - 1,
            self.maxelsize,
        ):
            posentry.set_max(pos)
            scale.configure(from_=math.floor(pos))
            voielsizeentry.set_max(elsize)
            if pos == 0:
                voishapeentry.set_max(0)
            elif voiposentry.get():
                voishapeentry.set_max(
                    math.floor(
                        (posentry.maxval + 1 - float(voiposentry.get()))
                        * elsize
                        / (posentry.maxval + 1)
                        / float(voielsizeentry.get())
                    )
                )
                voiposentry.set_max(
                    posentry.maxval
                    + 1
                    - float(voielsizeentry.get()) / (elsize / (posentry.maxval + 1))
                )
            else:
                voishapeentry.set_max(pos + 1)
                voiposentry.set_max(pos)

    def check_enable(self):
        if self.get_selected_imgs():
            state = "enabled"
        else:
            state = "disabled"
            self.default_vars()

        for item in [
            *self.imgpos.entries,
            *self.imgpos.scales,
            *self.voiinfo.posentries,
            *self.voiinfo.shapeentries,
            *self.voiinfo.elsizeentries,
            self.options.crosshaircheck,
            self.options.voicheck,
            self.options.zoomcheck,
        ]:
            item.config(state=state)

    def get_sampleshape(self):
        return np.array([s.get() for s in self.sampleshape])

    def set_sampleshape(self, vals):
        [s.set(val) for s, val in zip(self.sampleshape, vals)]

    def push_allinfo(self):
        for i in range(3):
            self.push_pos(i)
            self.push_voipos(i)
            self.push_voishape(i)
            self.push_voielsize(i)

    def push_pos(self, i):
        entries = self.imgpos.entries

        if entries[i].get():
            myimgs = self.get_selected_imgs()
            if myimgs:
                primary_img = myimgs[0]
            for myimg in myimgs:
                myimg.position.ravel()[i] = (
                    self.get_pos(i) * primary_img.affine.scale()[i]
                )

            [
                self.tra_update,
                self.cor_update,
                self.sag_update,
            ][i]()

    def tra_update(self):
        self.traframe.refresh()
        if self.traframe.image:
            self.corframe.canvas.draw_crosshairs()
            self.sagframe.canvas.draw_crosshairs()

    def cor_update(self):
        self.corframe.refresh()
        if self.corframe.image:
            self.traframe.canvas.draw_crosshairs()
            self.sagframe.canvas.draw_crosshairs()

    def sag_update(self):
        self.sagframe.refresh()
        if self.sagframe.image:
            self.traframe.canvas.draw_crosshairs()
            self.corframe.canvas.draw_crosshairs()

    def push_voipos(self, i):
        update = self.voiinfo.posentries[i].get()
        for myimg in self.get_selected_imgs():
            if update:
                myimg.voi.pos.ravel()[i] = (
                    self.voi["pos"][i].get()
                    * self.get_selected_imgs()[0].affine.scale()[i]
                )
                [
                    self.traframe,
                    self.corframe,
                    self.sagframe,
                ][i].canvas.draw_voi()
        return update

    def push_voishape(self, i):
        update = self.voiinfo.shapeentries[i].get()
        for myimg in self.get_selected_imgs():
            myimg.voi.shape.ravel()[i] = self.voi["shape"][i].get()
            [
                self.traframe,
                self.corframe,
                self.sagframe,
            ][i].canvas.draw_voi()
        return update

    def push_voielsize(self, i):
        update = self.voiinfo.elsizeentries[i].get()
        for myimg in self.get_selected_imgs():
            if update:
                myimg.voi.elsize.ravel()[i] = self.voi["elsize"][i].get()
                [
                    self.traframe,
                    self.corframe,
                    self.sagframe,
                ][i].canvas.draw_voi()
        return update

    def get_voi(self):
        pos, shape, elsize = [
            [x.get() for x in self.voi[field]] for field in ["pos", "shape", "elsize"]
        ]
        return img.VOI(shape=shape, pos=pos, elsize=elsize)

    def set_voi(self, voi):

        for entries, field in zip(
            [
                self.voiinfo.posentries,
                self.voiinfo.shapeentries,
                self.voiinfo.elsizeentries,
            ],
            ["pos", "shape", "elsize"],
        ):
            new_values = getattr(voi, field).ravel()
            scales = self.get_selected_imgs()[0].affine.scale()
            for entry, new_value, scale in zip(entries, new_values, scales):
                if field is "pos":
                    entry.set(new_value / scale)
                else:
                    entry.set(new_value)

    def get_pos(self, i=None):
        if i is None:
            return np.array([x.get() for x in self.pos]).reshape(-1, 1)
        else:
            return self.pos[i].get()

    def set_pos(self, pos: np.ndarray):
        [x.set(val) for x, val in zip(self.imgpos.entries, pos.ravel())]

    def default_samplerate(self, frame="original", voi=None):
        if voi is None:
            maxspace = img.utils.script.maxshape(
                *self.get_selected_imgs(), frame=frame
            )  # um
        else:
            maxspace = voi.shape * voi.elsize
        if not np.max(maxspace):
            self.samplerate.set(1)
        else:
            screenspace = maxspace[0] + maxspace[1], maxspace[0] + maxspace[2]  # um
            height_maxrate = self.winfo_screenheight() / screenspace[0]  # px / um
            width_maxrate = self.winfo_screenwidth() / screenspace[1]  # px / um
            self.samplerate.set(min(height_maxrate, width_maxrate) * 0.75)  # px / um
            if not self.samplerate.get():
                self.samplerate.set(1)

    def generate_voi(self):
        if self.flag_zoom.get():  # perform cropping operation on view
            voi = self.get_voi()
            self.default_samplerate(voi=voi)
            primary = self.get_selected_imgs()[0]

            pos = voi.pos.ravel() * primary.affine.scale()
            elsize = np.array([1.0, 1.0, 1.0]) / self.samplerate.get()
            shape = np.round(voi.shape * voi.elsize / elsize)
            return img.VOI(shape=shape, pos=pos, elsize=elsize)
        else:  # default voi
            pos = np.zeros(3)
            elsize = np.array([1.0, 1.0, 1.0]) / self.samplerate.get()
            primary = self.get_selected_imgs()[0]

            shapes = []
            for myimg in self.get_selected_imgs():
                shapes.append(np.round(myimg.shape * myimg.affine.scale() / elsize))
            shape = np.array(shapes).max(0)
            return img.VOI(shape=shape, pos=pos, elsize=elsize)


class Popup(tk.Toplevel):
    def __init__(self, master, title, func, **fields):
        """
        **fields = {
            parameterLabel: [
                tkClass,**tkclass_kwargs
            ]
        }
        """
        super().__init__(master)
        self.resizable(height=False, width=False)
        self.frame = tk.LabelFrame(self, text=f"{title} Parameters")
        self.func = func
        self.subframes = []
        self.vars = {}
        self.imgname = tk.StringVar()
        self.generate(**fields)
        self.grab_set()

    def generate(self, **fields):
        self.frame.pack(padx=15, pady=10)

        i = 0
        for i, (field, components) in enumerate(fields.items()):
            label, parts = components
            tk.Label(self.frame, text=f"{label}:").grid(row=i + 1, column=0, sticky="e")
            self.subframes.append(tk.Frame(self.frame))
            self.subframes[i].grid(row=i + 1, column=1)
            self.vars[field] = []
            for j, part in enumerate(parts):
                compclass, default, kwargs = part
                self.vars[field].append(compclass(self.subframes[i], **kwargs))
                self.vars[field][j].bind(
                    "<Return>", lambda *args: self.release_from(self.vars[field][j])
                )
                self.vars[field][j].set(default)
                self.vars[field][j].grid(row=0, column=j)

        selections = [
            selection
            for selection in self.master.get_selected_imgnames()
            if selection is not "None"
        ]

        tk.Label(self.frame, text="Image:").grid(row=0, column=0, sticky="e")
        OptionMenu(self.frame, self.imgname, selections[0], *selections).grid(
            row=0, column=1
        )
        ttk.Button(self.frame, text="Ok", command=self.release).grid(
            row=i + 2, column=0, columnspan=2
        )

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(i + 2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.update()
        geometry = self.geometry()
        split = tools.multisplit(geometry, *"+x")
        if int(split[0]) < 150:
            split[0] = "150"
        if int(split[1]) < 50:
            split[1] = "50"
        self.geometry(f"{split[0]}x{split[1]}+{split[2]}+{split[3]}")

    def get_params(self):
        """
        Defines kwargs.
        """
        params = {}
        for varname, varvals in self.vars.items():
            if len(varvals) >= 2:
                params[varname] = []
                for val in varvals:
                    params[varname].append(val.var.get())
            else:
                params[varname] = varvals[0].var.get()
        return params

    def get_func(self):
        selected_img_ind = self.master.get_selected_imgnames().index(self.imgname.get())
        selected_img = self.master.get_selected_imgs()[selected_img_ind]
        if "." in self.func:
            funcname = self.func.split(".")[-1]
            func_groups = self.func
        else:
            funcname = self.func

        while "." in func_groups:
            func_groups = func_groups.split(".")
            selected_img = getattr(selected_img, func_groups[0])
            func_groups = ".".join(func_groups[1:])
        return getattr(selected_img, funcname)

    def release_from(self, child):
        child.var.set(child.get())
        self.release()

    def release(self):
        self.grab_release()
        self.withdraw()
        func = self.get_func()
        params = self.get_params()

        self.master.progressbar.run(func, **params)
        self.master.refresh()
        self.destroy()
