# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-05-28 18:03:59
@LastEditTime: 2021-09-02 10:18:14
@LastEditors: HuangJianYi
:description: 主题皮肤
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.theme.theme_info_model import *
from seven_cloudapp.models.db_models.skin.skin_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *

from seven_cloudapp.handlers.server.theme_s import SkinListHandler
from seven_cloudapp.handlers.server.theme_s import ThemeUpdate


class ThemeListHandler(SevenBaseHandler):
    """
    :description: 主题列表
    """
    def get_async(self):
        """
        :description: 主题列表
        :param 
        :return: 列表
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        where = "is_release=1"
        params = []
        power_menu_list = self.get_power_menu(app_id)
        if len(power_menu_list)>0:
            for i in power_menu_list:
                if i in [322922329844087484,500255366806462773]:
                    where += " and app_id=%s"
                    params.append(app_id)
                    break
        if len(params)<=0:
            where += " and app_id=''"
        dict_list = ThemeInfoModel(context=self).get_dict_list(where, params=params)

        for dict_info in dict_list:
            dict_info["client_json"] = self.json_loads(dict_info["client_json"]) if dict_info["client_json"] else {}
            dict_info["server_json"] = self.json_loads(dict_info["server_json"]) if dict_info["server_json"] else {}

        self.reponse_json_success(dict_list)