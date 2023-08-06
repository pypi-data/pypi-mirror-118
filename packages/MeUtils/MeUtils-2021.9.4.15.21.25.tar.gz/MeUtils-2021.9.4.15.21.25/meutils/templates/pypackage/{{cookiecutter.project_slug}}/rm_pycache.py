#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : nlpzoo.
# @File         : rm_pycache
# @Time         : 2021/9/4 下午3:18
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *


def rm_pycache(dir_home='{{ cookiecutter.project_slug }}'):
    ps = Path(dir_home).glob('*')
    for p in ps:
        if p.name == '__pycache__':
            cmd = f"rm -rf {p.absolute()}"
            logger.info(cmd)
            os.system(cmd)

        elif p.is_dir():
            rm_pycache(p)


if __name__ == '__main__':
    rm_pycache()
