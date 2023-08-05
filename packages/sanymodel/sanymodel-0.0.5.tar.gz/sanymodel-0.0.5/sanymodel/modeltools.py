# -*- coding: utf-8 -*-
# @Time : 2021/8/24 19:11
# @Author : gaozq
# @File : modeltools.py
# @Software: PyCharm
# @contact: gaozq3@sany.com.cn
# -*- 功能说明 -*-
#
# -*- 功能说明 -*-

import os
import sys
import json
import logging
import pandas as pd
import traceback
from arrow import now
from sanydata import datatools
from sanymodel.metaclass import *
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler


class Result(object):
    """
    结果回传数据类
    :return:
    """

    def __init__(self, wind_farm: str, turbine_num: str, data_start_time: str, data_end_time: str,
                 project_name: str = None, model_version: str = None, data_start_time_real: str = None,
                 data_end_time_real: str = None, stub: str = None):
        assert len(data_start_time) > 9, '日期格式不正确'
        assert len(data_end_time) > 9, '日期格式不正确'

        self.wind_farm = wind_farm
        self.turbine_num = turbine_num
        self.data_start_time = data_start_time
        self.data_end_time = data_end_time
        self.data_start_time_real = data_start_time_real or data_start_time[:10] + ' 00:00:00'
        self.data_end_time_real = data_end_time_real or data_start_time[:10] + ' 00:00:00'

        self.project_name = project_name or 'Result'
        self.model_version = model_version or '1.0.0'

        self.local_fig_paths = []
        self.upload_fig_paths = []
        self.fig_names = []
        self.fig_datas = []

        self.local_file_paths = []
        self.upload_file_paths = []

        self.status = '正常'
        self.result = '正常'
        self.comment = '正常'
        self.description = '正常'

        self.warnings = []
        self.errors = []

        self.stub = stub
        self.result_json = self.format_json()

    def format_json(self):
        result_json = dict()
        result_json['custom'] = dict()
        result_json['mainData'] = dict()
        result_json['subPics'] = list()
        result_json['custom']['real_start_time'] = self.data_start_time_real
        result_json['custom']['real_end_time'] = self.data_end_time_real
        return result_json

    def add_fig(self, local_fig_path: str, upload_fig_path: str = None, fig_name: str = None, fig_data: str = '',
                rename=False, main=False):
        """
        上传结果
        :param local_fig_path:
        :param upload_fig_path:
        :param fig_name:
        :param fig_data:
        :param rename:
        :param main:
        :return:
        """
        assert os.path.exists(local_fig_path), '图像不存在'
        assert self.project_name != 'Result', 'project_name未指定'
        assert self.turbine_num, 'turbine_num未指定'

        file_name = local_fig_path.split('/')[-1].split('.')[0]
        file_type = local_fig_path.split('/')[-1].split('.')[-1]

        if not fig_name:
            fig_name = local_fig_path.split('/')[-1].split('.')[0]

        if rename:
            name_parts = [self.wind_farm, self.turbine_num, self.data_start_time, self.data_end_time, fig_name]
            file_name = '_'.join(name_parts)

        if not upload_fig_path:
            upload_fig_path = 'fig/{}/{}/{}.{}'.format(self.project_name, self.wind_farm, file_name, file_type)

        fs = [local_fig_path, upload_fig_path, fig_name, fig_data]
        ls = [self.local_fig_paths, self.upload_fig_paths, self.fig_names, self.fig_datas]

        for f, l in zip(fs, ls):
            if main:
                l.insert(0, f)
            else:
                l.append(f)

        return local_fig_path, upload_fig_path, fig_name, fig_data

    def add_file(self, local_file_path: str, upload_file_path: str = None, rename=False):
        """
        上传结果
        :param local_file_path:
        :param upload_file_path:
        :param rename:
        :return:
        """
        assert os.path.exists(local_file_path), '文件不存在'
        assert self.project_name != 'Result', 'project_name未指定'
        assert self.turbine_num, 'turbine_num未指定'

        file_name = local_file_path.split('/')[-1].split('.')[0]
        file_type = local_file_path.split('/')[-1].split('.')[-1]

        if rename:
            name_parts = [self.wind_farm, self.turbine_num, self.data_start_time, self.data_end_time, file_name]
            file_name = '_'.join(name_parts)

        if not upload_file_path:
            upload_file_path = 'file/{}/{}/{}.{}'.format(self.project_name, self.wind_farm, file_name, file_type)

        self.local_fig_paths.append(local_file_path)
        self.upload_file_paths.append(upload_file_path)

        return local_file_path, upload_file_path

    def add_warning(self, warning):
        self.warnings.append(warning)
        self.status = '告警'

    def add_error(self, error):
        self.errors.append(error)
        self.status = '故障'

    def upload(self, stub: str = None):
        """
        上传结果
        :param stub:
        :return:
        """
        assert self.project_name != 'Result', 'project_name未指定'
        assert self.turbine_num, 'turbine_num未指定'
        assert len(self.local_fig_paths) == len(self.upload_fig_paths) == len(self.fig_names) == len(
            self.fig_datas), '待上传图像数据长度不一致'
        assert len(self.local_file_paths) == len(self.upload_file_paths), '待上传文件数据长度不一致'
        stub = stub or self.stub
        assert stub, 'grpc地址未传入'

        dt = datatools.DataTools()

        if len(self.upload_fig_paths) > 1:
            put_file_result = dt.put_files(stub, self.local_fig_paths[1:], self.upload_fig_paths[1:])
            for path, name, data, in zip(put_file_result, self.fig_names[1:], self.fig_datas[1:]):
                if 'put_file error' not in path:
                    self.result_json['subPics'].append({'name': name,
                                                        'data': data,
                                                        'path': path
                                                        })
                else:
                    err = '{}_{} put sub png {} error, {}'.format(self.wind_farm,
                                                                  self.turbine_num,
                                                                  path,
                                                                  name)
                    raise RuntimeError(err)

        if len(self.upload_file_paths) > 1:
            put_file_result = dt.put_files(stub, self.local_file_paths[1:], self.upload_file_paths[1:])
            for path, local_path, in zip(put_file_result, self.local_file_paths[1:]):
                if 'put_file error' not in path:
                    self.result_json['subFiles'].append({'name': local_path, })
                else:
                    err = '{}_{} put sub file {} error, {}'.format(self.wind_farm,
                                                                   self.turbine_num,
                                                                   path,
                                                                   local_path)
                    raise RuntimeError(err)

        u = l = d = n = fu = fl = ''

        if len(self.upload_fig_paths):
            u, l, d, n = list(zip(self.upload_fig_paths, self.local_fig_paths, self.fig_datas, self.fig_names))[0]

        if len(self.upload_file_paths):
            fu, fl = list(zip(self.upload_file_paths, self.local_file_paths))[0]

        self.result_json['mainData']['name'] = n
        self.result_json['mainData']['data'] = d

        if self.warnings:
            if (self.comment == '正常') & (self.description == '正常'):
                if self.errors:
                    self.comment = '故障:' + ','.join(self.errors) + '; 告警:' + ','.join(self.warnings)
                else:
                    self.comment = '告警:' + ','.join(self.warnings)
                self.description = self.comment

        code = dt.return_result(stub=stub,
                                project_name=self.project_name,
                                model_version=self.model_version,
                                wind_farm=self.wind_farm,
                                data_start_time=self.data_start_time,
                                data_end_time=self.data_end_time,
                                turbine_num=self.turbine_num,
                                upload_fig_path=u,
                                local_fig_path=l,
                                upload_file_path=fu,
                                local_file_path=fl,
                                result_json=json.dumps(self.result_json),
                                status=self.status,
                                result=self.result,
                                comment=self.comment,
                                description=self.description
                                )
        msg = '{} 风场 {} 风机 {} 至 {} {} 上传状态为{}'.format(self.wind_farm,
                                                      self.turbine_num,
                                                      self.data_start_time_real,
                                                      self.data_end_time_real,
                                                      self.comment,
                                                      code)
        if code:
            raise RuntimeError(msg)

        return msg


class Logger:
    def __init__(self, project_name, model_version, stub):
        file_name = '{}.log'.format(project_name)
        log_path = '/tmp/log/'
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        self.project_name = project_name
        self.model_version = model_version
        self.stub = stub
        self.local_path = log_path + file_name
        logging.basicConfig()
        self.logger = logging.getLogger(project_name)
        self.logger.setLevel(logging.INFO)
        # 日志格式
        fmt = logging.Formatter(
            '[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s]: %(message)s',
            '%Y-%m-%d %H:%M:%S')

        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)
        self.logger.propagate = False
        if file_name is not None:
            tf = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, file_name),
                                                           when='D',
                                                           backupCount=14)
            tf.suffix = "%Y-%m-%d"
            tf.setFormatter(fmt)
            tf.setLevel(logging.INFO)
            self.logger.addHandler(tf)

    @property
    def get_log(self):
        return self.logger

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)

    def upload(self):
        """
        销毁对象上传日志
        :return:
        """
        dt = datatools.DataTools()
        time_now = now().strftime('%Y_%m_%d_%H_%M_%S')
        upload_log_path = 'log/{}/{}.log'.format(self.project_name, time_now)
        self.logger.info('上传日志: {}'.format(upload_log_path))
        dt.return_result(self.stub,
                         project_name=self.project_name,
                         model_version=self.model_version,
                         wind_farm='log',
                         data_start_time=time_now,
                         data_end_time=time_now,
                         upload_log_path=upload_log_path,
                         local_log_path='/tmp/log/{}.log'.format(self.project_name)
                         )


class Tag(object):

    def __init__(self, name: str, data_type: str, usage: str = 'user_defined', creator: str = '',
                 description: str = '', ):
        self.name = name
        self.data_type = data_type
        self.usage = usage
        self.creator = creator
        self.description = description
        self.meta_folder = 'tag_meta'
        self.tag_folder = 'Tag'

    def register(self, name: str = None, data_type: str = None, usage: str = None, creator: str = None,
                 description: str = None,
                 stub: str = 'localhost:50051'):
        """
        不要放在模型运行代码中！
        :param self:
        :param name:
        :param data_type:
        :param usage:
        :param creator:
        :param description:
        :param stub:
        :return:
        """
        name = name or self.name
        data_type = data_type or self.data_type
        usage = usage or self.usage
        creator = creator or self.creator
        description = description or self.description

        col_name = ['Name', 'Datatype', 'Usage', 'Creator', 'Description']
        line = [[name, data_type, usage, creator, description]]
        tag_new = pd.DataFrame(data=line, columns=col_name, )
        tag_ori = self.query()
        tag_merged = pd.concat([tag_new, tag_ori]).drop_duplicates()

        tag_merged.to_csv('/tmp/tag.csv', encoding='gbk', index_label=False)
        dt = datatools.DataTools()
        f = dt.put_files(stub=stub,
                         local_files=['/tmp/tag.csv'],
                         database=True,
                         project_name='tag_meta',
                         data_time=None,
                         wind_farm=None,
                         turbine_type=None,
                         turbine_num=None,
                         file_type='file')

    @staticmethod
    def query(name: str = None, data_type=None, usage=None, creator=None, description: str = None,
              stub: str = 'localhost:50051'):
        """
        不要放在模型运行代码中！
        :param self:
        :param name:
        :param data_type:
        :param usage:
        :param creator:
        :param description:
        :param stub:
        :return:
        """
        dt = datatools.DataTools()
        tag_info = dt.get_self_files(stub=stub,
                                     project_name='tag_meta',
                                     farm=None,
                                     turbine_type=None,
                                     turbine=None)

        tag_meta = dt.get_data(stub=stub, file_list=tag_info, data_type='self')
        return tag_meta

    def upload(self, series: pd.Series, wind_farm: str = None, turbine_num: str = None, turbine_type: str = None,
               stub: str = 'localhost:50051'):
        assert isinstance(series, pd.Series), '只接受 pd.Series'
        assert isinstance(series.index, pd.DatetimeIndex), '只接受 pd.DatetimeIndex'
        assert (isinstance(series.dtype, pd.CategoricalDtype) | isinstance(series.dtype, pd.BooleanDtype)), '只接受 pd.BooleanDtype or pd.CategoricalDtype'
        days = series.index.strftime('%Y-%m-%d').unique()
        dt = datatools.DataTools()
        upload_paths = []
        if not os.path.exists('/tmp/tag'):
            os.makedirs('/tmp/tag')
        for day in days:
            subset = series.loc[day]
            # TODO: sanydata添加pickle读写方式
            # local_path = fr'/tmp/tag/{wind_farm}_{turbine_type}_{turbine_num}_{self.name}_{self.data_type}_{day}.pkl'
            # subset.to_pickle(local_path)
            local_path = fr'/tmp/tag/{wind_farm}_{turbine_type}_{turbine_num}_{self.name}_{self.data_type}_{day}.pkl'
            subset.to_csv(local_path, encoding='gbk', index_label=False)
            upload_path = dt.put_files(stub=stub,
                                       local_files=[local_path],
                                       database=True,
                                       project_name=self.tag_folder,
                                       data_time=day,
                                       wind_farm=wind_farm,
                                       turbine_type=turbine_type,
                                       turbine_num=turbine_num,
                                       file_type='file')
            upload_paths.extend(upload_path)
        return upload_paths

    def download(self, name: str, data_type: str, start_time=None, end_time=None, wind_farm: str = None,
                 turbine_num: str = None, turbine_type: str = None, stub: str = 'localhost:50051'):
        dt = datatools.DataTools()
        tag_file = dt.get_self_files(stub,
                                     project_name=self.tag_folder,
                                     farm=wind_farm,
                                     turbine_type=turbine_type,
                                     turbine=turbine_num,
                                     start_time=start_time,
                                     end_time=end_time)

        tag_selctor = fr'{name}_{data_type}'
        tag_file = [f for f in tag_file if (f.find(tag_selctor) != -1)]
        if not tag_file:
            return tag_file
        tag_data = dt.get_data(stub=stub, file_list=tag_file, data_type='self')
        return tag_data


class SensorErrorTag(Tag):

    def __init__(self, field: str, name: str, data_type: str, usage: str = 'user_defined', creator: str = '',
                 description: str = '', ):
        self.field = Field(field, data_type)
        super(SensorErrorTag, self).__init__(name, data_type, usage, creator, description)
        self.tag_folder = 'SensorErrorTag'
        print(self.__dict__)


class Record(object):

    def __init__(self, name: str, data_type: str, usage: str = 'user_defined', creator: str = '',
                 description: str = '', ):
        self.name = name
        self.data_type = data_type
        self.usage = usage
        self.creator = ''
        self.description = ''
        self.cols = ['Begin', 'End']

    @staticmethod
    def register(self, name: str, data_type: str, usage: str, creator: str, description: str,
                 stub: str = 'localhost:50051'):
        """

        :param self:
        :param name:
        :param data_type:
        :param usage:
        :param creator:
        :param description:
        :param stub:
        :return:
        """
        col_name = ['Name', 'Datatype', 'Usage', 'Creator', 'Description', 'Fields']
        line = [[self.name, self.data_type, self.usage, self.creator, self.description, ','.join(self.cols)]]
        tag_new = pd.DataFrame(data=line, columns=col_name, )
        tag_ori = self.query()
        tag_merged = pd.concat([tag_new, tag_ori]).drop_duplicates()

        tag_merged.to_csv('/tmp/record.csv', encoding='gbk', index_label=False)
        dt = datatools.DataTools()
        f = dt.put_files(stub=stub,
                         local_files=['/tmp/record.csv'],
                         database=True,
                         project_name='record_meta',
                         data_time=None,
                         wind_farm=None,
                         turbine_type=None,
                         turbine_num=None,
                         file_type='file')

    @staticmethod
    def query(self, name: str = None, data_type=None, usage=None, creator=None, description: str = None,
              stub: str = 'localhost:50051'):
        """

        :param self:
        :param name:
        :param data_type:
        :param usage:
        :param creator:
        :param description:
        :param stub:
        :return:
        """
        dt = datatools.DataTools()
        record_info = dt.get_self_files(stub=stub,
                                        project_name='record_meta',
                                        farm=None,
                                        turbine_type=None,
                                        turbine=None)

        record_meta = dt.get_data(stub=stub, file_list=record_info, data_type='self')
        return record_info


class ModelTool(object):

    def __init__(self, project_name, model_version, start_time, end_time,
                 grpcurl=os.getenv('grpcurl', 'localhost:50051')):
        self.project_name = project_name
        self.model_version = model_version
        self.start_time = start_time
        self.end_time = end_time
        # 初始化日志
        self.logger = Logger(project_name, model_version, grpcurl)
        self.logger.info('=' * 60)
        self.logger.info('=' * 60)
        ls = int((60 - (len(project_name) + len(model_version) + 15)) / 2)
        self.logger.info('{} {} ver {} initial {}'.format('=' * ls, project_name, model_version, '=' * ls))
        # 初始化数据工具
        self.grpcurl = grpcurl
        self.logger.info('grpcurl:{}'.format(self.grpcurl))
        self.dt = datatools.DataTools()
        self.logger.info('数据开始时间:{}'.format(start_time))
        self.logger.info('数据结束时间:{}'.format(end_time))
        self.logger.info('=' * 60)
        self.logger.info('=' * 60)

    def create_turbine_result(self, wind_farm, turbine_num, start_time=None, end_time=None):
        if not start_time:
            start_time = self.start_time
        if not end_time:
            end_time = self.end_time

        return Result(wind_farm=wind_farm,
                      turbine_num=turbine_num,
                      data_start_time=start_time,
                      data_end_time=end_time,
                      project_name=self.project_name,
                      model_version=self.model_version,
                      stub=self.grpcurl)

    def create_farm_result(self, wind_farm, start_time=None, end_time=None):
        if not start_time:
            start_time = self.start_time
        if not end_time:
            end_time = self.end_time

        return Result(wind_farm=wind_farm,
                      turbine_num='farm',
                      data_start_time=start_time,
                      data_end_time=end_time,
                      project_name=self.project_name,
                      model_version=self.model_version,
                      stub=self.grpcurl)

    def create_logger(self):
        return self.logger


# t = ModelTool('Test', '1.0.0', '2021-01-01', '2021-02-01')
# r = t.create_turbine_result('ALSFC', '001')
# t.c
# r.add_warning('有问题')
# # r.upload()
# l = t.create_logger()
# r.add_error()
# r.add_fig(local_fig_path='/tmp/1.png')

# l.info('b')
# l.upload()
# print(r.__dict__)
# l.upload()
#
# r.add_file()

# t = Tag('测试', 'second', )
# t.register(creator=None, description=None)
# t.register(creator='Tag', description='测试标签1')
# print(t.query())

# dt = datatools.DataTools()
# f = dt.get_files('localhost:50051', 'TYSFCB', 'second', '2021-01-01', '2021-01-02', '001')
# d = dt.get_data('localhost:50051', f, ['time', '风速1'])
# d['time'] = pd.to_datetime(d['time'])
# tag1 = d['风速1'] < 3
# tag1.index = d['time']
#
# bin = [5, 10, 20]
# tag2 = pd.cut(d['风速1'], bins=bin, labels=['小', '大'])
# tag2.index = d['time']
# tag2.to_pickle('/tmp/tag2.pkl')
#
# a = t.upload(tag2, 'ALSFC', '001')
# print(a)
#
# z = t.download( name='测试', data_type='second', start_time='2021-01-01', end_time='2021-01-01', wind_farm='ALSFC')
# print(z)
#
# tag3 = pd.read_pickle('/tmp/tag2.pkl')
#
# print(tag2[(tag2!='小') & (tag2!='大')])
#
# print(tag3.value_counts())


# print(tag1[tag1])
# print(tag1)
# print(d)
# s = pd

# Tag.upload()

# t = SensorErrorTag(field='轴1电机温度', name='变桨电机温度超阈值', data_type='second', usage='SensorError', creator='Tag',
#                    description='温度传感器异常的标签')
# t.register()
# print(t.query())
#
# dt = datatools.DataTools()
# f = dt.get_files('localhost:50051', 'TYSFCB', 'second', '2021-01-01', '2021-01-02', '001')
# d = dt.get_data('localhost:50051', f, ['time', '轴1电机温度'])
#
# d['time'] = pd.to_datetime(d['time'])
# tag1 = d['轴1电机温度'] > 100
# tag1.index = d['time']
# tag1 = tag1.astype('boolean')
#
#
# t.upload(tag1, wind_farm='TYSFCB', turbine_num='001')
# q = t.download(name='变桨电机温度', data_type='second', start_time='2021-01-01', end_time='2021-01-02')
# # q = q.astype('boolean')
# print(q)
