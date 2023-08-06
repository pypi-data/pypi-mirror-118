# -*- coding: utf-8 -*-
import argparse
import json
import os
import time
from datetime import datetime, timedelta

from dailycheckin.__version__ import __version__
from dailycheckin.configs import checkin_map, get_checkin_info, get_notice_info
from dailycheckin.motto.motto import Motto
from dailycheckin.utils.message import push_message


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--include", nargs="+", help="任务执行包含的任务列表")
    parser.add_argument("--exclude", nargs="+", help="任务执行排除的任务列表")
    return parser.parse_args()


def checkin():
    args = parse_arguments()
    include = args.include
    exclude = args.exclude
    print(f"当前 Pypi 版本: {__version__}")
    if not include:
        include = list(checkin_map.keys()) + ["MOTTO"]
    else:
        include = [one for one in include if one in checkin_map.keys()]
    if not exclude:
        exclude = []
    else:
        exclude = [one for one in exclude if one in checkin_map.keys()]
    task_list = list(set(include) - set(exclude))
    task_name_str = "\n".join([checkin_map.get(one)[0] for one in task_list if one != "MOTTO"])
    if "MOTTO" in task_list:
        task_name_str += "\n每日一句"
    print(f"---------- 本次执行签到任务如下 ----------:\n{task_name_str}\n\n")
    start_time = time.time()
    utc_time = datetime.utcnow() + timedelta(hours=8)
    config_path = None
    for one_path in [
        "/ql/scripts/config.json",
        "config.json",
        "../config.json",
        "./config/config.json",
        "../config/config.json",
    ]:
        _config_path = os.path.join(os.getcwd(), one_path)
        if os.path.exists(_config_path):
            config_path = os.path.normpath(_config_path)
            break
    if config_path:
        print("使用配置文件路径:", config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        try:
            motto = data.get("MOTTO")
            notice_info = get_notice_info(data=data)
            check_info = get_checkin_info(data=data)
        except Exception as e:
            raise e
        content_list = [f"当前时间: {utc_time}"]
        for one_check, check_tuple in checkin_map.items():
            if one_check in task_list:
                check_name, check_func = check_tuple
                if check_info.get(one_check.lower()):
                    print(f"----------已检测到正确的配置，并开始执行【{check_name}】签到----------")
                    for index, check_item in enumerate(check_info.get(one_check.lower(), [])):
                        print(f"----------开始执行【{check_name}】签到 : 第 {index + 1} 个账号----------")
                        if "xxxxxx" not in str(check_item) and "多账号" not in str(check_item):
                            try:
                                msg = check_func(check_item).main()
                                content_list.append(f"【{check_name}】\n{msg}")
                                print(f"----------执行完成 【{check_name}】签到 : 第 {index + 1} 个账号----------")
                            except Exception as e:
                                content_list.append(f"【{check_name}】\n{e}")
                                print(f"----------执行失败 【{check_name}】签到 : 错误日志如下:----------\n{e}")

                        else:
                            print(f"----------跳过执行【{check_name}】签到 : 配置文件包含自带的默认配置----------")
                else:
                    print(f"----------未检测到正确的配置，并跳过执行【{check_name}】签到----------")
        if motto and ((motto in include) or (motto not in exclude)):
            try:
                msg_list = Motto().main()
            except Exception as e:
                print(e)
                msg_list = []
            content_list += msg_list
        content_list.append(f"任务使用时间: {int(time.time() - start_time)} 秒")
        content_list.append(f"当前 Pypi 版本: {__version__}")
        push_message(content_list=content_list, notice_info=notice_info)
        return
    else:
        print("配置文件不存在")


if __name__ == "__main__":
    checkin()
