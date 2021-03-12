import Dahai
import Pon_Chii
import Kan
import Ok
import Riichi
import Agari
import Cancel
import Yoyaku
import Kyuusyu

gui_dic = {"Dahai":Dahai.Dahai, "Pon_Chii":Pon_Chii.Pon_Chii, "Kan":Kan.Kan, "Ok":Ok.Ok,\
     "Riichi":Riichi.Riichi, "Agari":Agari.Agari, "Cancel":Cancel.Cancel, "Yoyaku":Yoyaku.Yoyaku, "Kyuusyu":Kyuusyu.Kyuusyu}


def gui_click(key, arg=None):
    if arg is None:
        gui_dic[key]()
    else:
        gui_dic[key](arg)

