import xml.etree.ElementTree as Xml
import tkinter as tk


class XmlWrapperError(Exception):
    pass


class AdvancedGui:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self._all_available_kwargs = ["xml_file", "css_file", "shared_globals", "functions"]
        self._kwargs_fix = {"xml_file": None, "css_file": None, "shared_globals": None, "functions": {}}
        for i in self._all_available_kwargs:
            try:
                self.kwargs[i]
            except KeyError:
                self.kwargs[i] = self._kwargs_fix[i]
        self.shared_globals = self.kwargs["shared_globals"]

    def load_xml(self):
        self.change_xml = {"color": "bg",
                           "bordercolor": "highlightbackground",
                           "bordercolorwidth": "highlightthickness",
                           "activecolor": "activebackground",
                           "textcolor": "foreground",
                           "activetextcolor": "activeforeground",
                           "disabledtextcolor": "disabledforeground",
                           "activebordercolor": "highlightcolor"}
        if self.kwargs["xml_file"] is not None:
            try:
                tree = Xml.parse(self.kwargs["xml_file"])
                error = False
            except Xml.ParseError:
                error = True
            if error:
                raise XmlWrapperError("Please check your xml file again!")
            tree_root = tree.getroot()
            guis = {}    
            mains = []
            mains_data = []
            for i in tree_root:
                gui_object = str(i.attrib["object"]) + "("
                for attrib in i.attrib:
                    if attrib != "object":
                        if attrib == "master":
                            gui_object += str(i.attrib[attrib]) + ","
                        elif attrib == "font":
                            if "(" in i.attrib[attrib]:
                                att = eval(i.attrib[attrib])
                                gui_object += "font=("
                                for u in att:
                                    if type(u) == str:
                                        gui_object += f"'{u}',"
                                    else:
                                        gui_object += f"{u},"
                                gui_object = gui_object[:-1]
                                gui_object += "),"
                            else:
                                gui_object += "font=" + str(i.attrib[attrib]) + ", "
                        else:
                            if attrib in list(self.change_xml.keys()):
                                attrib2 = self.change_xml[attrib]
                            else:
                                attrib2 = attrib
                            gui_object += f"{attrib2}=\'{i.attrib[attrib]}\', "
                gui_object += ")"
                guis[f"{i.tag} = tk.{gui_object}"] = []
                for ii in i:
                    if ii.tag == "bind" or ii.tag == "bind_all":
                        test = ii.text
                        test = f"'<{list(ii.attrib.items())[0][1]}>', {test}"
                    else:
                        test = ii.text
                        for a in list(self.change_xml.keys()):
                            if a in test:
                                raise XmlWrapperError(f"Keyword {a} in {ii.tag} is still not supported!")
                    guis[f"{i.tag} = tk.{gui_object}"].append(f"{i.tag}.{ii.tag}({test})")
            for i in list(guis.items()):
                mains.append(i[0])
                for ii in i[1]:
                    mains_data.append(ii)
            return mains, mains_data
