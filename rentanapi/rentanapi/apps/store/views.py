from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from tablestore import OTSClient, PK_AUTO_INCR, TableMeta, TableOptions, ReservedThroughput, CapacityUnit, Row, \
    Condition, RowExistenceExpectation, PutRowItem, BatchWriteRowRequest, TableInBatchWriteRowItem, Direction, INF_MIN, \
    INF_MAX


class TableAPIView(APIView):
    @property
    def client(self):
        return OTSClient(settings.OTSClient, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)
    def post(self,request):
        """创建表"""
        # 设置主键和字段
        table_name = 'user_message'
        # schema_of_primary_key = [
        #     ('字段名', '字段类型' , PK_AUTO_INCR),
        #     ('uid', 'STRING')
        # ]
        # 主键列
        schema_of_primary_key = [
            ('user_id', 'INTEGER'),
            ('sequence_id', 'INTRGER',PK_AUTO_INCR),
            ('sender_id', 'INTRGER'),
            ('message_id', 'INTRGER')
        ]
        # 设置表的元信息
        table_meta = TableMeta(table_name, schema_of_primary_key)
        # 设置数据的有效型
        table_option = TableOptions(7*86400,5)
        # 设置数据的预留读写吞吐量
        reserved_throughput = ReservedThroughput(CapacityUnit(0,0))
        # 创建数据
        self.client.create_table(table_meta, table_option, reserved_throughput)
        return Response({'message':'ok'})

    def delete(self, request):
        """删除表"""
        table = 'user_message_table'
        self.client.delete_table(table)
        return Response({'message':'ok'})

    def get(self,request):
        table_list = 'user_message_table'
        for table in table_list:
            print(table)
        return Response({'message':'ok'})


class DataAPIView(APIView):
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def post(self):
        """添加数据到表格中"""
        table_name = "user_message_table"
        # 主键列
        primary_key = [
            # ('主键名', 值)
            ('user_id', 3),
            ('sequence_id',PK_AUTO_INCR), # 自增用PK_AUTO_INCR
            ("sender_id", 1),
            ('message_id',4),
        ]

        attribute_columns = [("recevice_time", datetime.now().timestamp()), ('read_status',False)]
        row = Row(primary_key,attribute_columns)
        consumed, return_row = self.client.put_row(table_name, row)
        print(return_row)

        return Response({"message":"ok"})

    def get(self,response):
        """获取指定数据"""
        table_name = 'user_message_table'
        primary_key = [('user_id', 3),('sequence_id', 153555353535355), ('sender_id',1), ('message_id',4)]
        # 需要返回的属性列： 如果columns_to_get为[], 则返回所有属性列。
        columns_to_get = []
        # columns_to_get = ['recevice_time', 'age']
        consulmde, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)

        print(return_row.attribute_columns)
        # [('read_status', False, 1579393933939),('recevice_time',15578888888855, 15969696966996)]
        return Response({"message":"ok"})

class RowAPIView(APIView):
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    """多行数据操作"""
    """多行数据操作"""

    def get(self, request):
        """按范围获取多行数据"""

        table_name = "user_message_table"

        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', 3),
            ('sequence_id', INF_MIN),
            ('sender_id', INF_MIN),
            ('message_id', INF_MIN)
        ]

        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', 3),
            ('sequence_id', INF_MAX),
            ('sender_id', INF_MAX),
            ('message_id', INF_MAX)
        ]

        # 查询所有列
        columns_to_get = []  # 表示返回所有列
        limit = 5

        # 设置多条件
        # cond = CompositeColumnCondition(LogicalOperator.AND) # 逻辑条件
        # cond = CompositeColumnCondition(LogicalOperator.OR)
        # cond = CompositeColumnCondition(LogicalOperator.NOT)

        # 多条件下的子条件
        # cond.add_sub_condition(SingleColumnCondition("read_status", False, ComparatorType.EQUAL)) #  比较运算符:　等于
        # cond.add_sub_condition(SingleColumnCondition("属性列", '属性值', ComparatorType.NOT_EQUAL)) #  比较运算符:　不等于
        # cond.add_sub_condition(SingleColumnCondition("属性列", '属性值', ComparatorType.GREATER_THAN)) #  比较运算符:　大于
        # cond.add_sub_condition(SingleColumnCondition("recevice_time", 1579246049, ComparatorType.GREATER_EQUAL)) #  比较运算符:　大于等于
        # cond.add_sub_condition(SingleColumnCondition("属性列", '属性值', ComparatorType.LESS_THAN)) #  比较运算符:　小于
        # cond.add_sub_condition(SingleColumnCondition("recevice_time", 1579246049, ComparatorType.LESS_EQUAL)) #  比较运算符:　小于等于

        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            limit,  # 结果数量
            # column_filter=cond, # 条件
            max_version=1  # 返回版本数量
        )

        print("一共返回了：%s" % len(row_list))

        for row in row_list:
            print(row.primary_key, row.attribute_columns)

        return Response({"message": "ok"})

    def post(self, request):
        """添加多条数据"""

        table_name = "user_message_table"

        put_row_items = []

        for i in range(0, 10):
            # 主键列
            primary_key = [  # ('主键名', 值),
                ('user_id', i),  # 接收Feed的用户ID
                ('sequence_id', PK_AUTO_INCR),  # 如果是自增主键，则值就是 PK_AUTO_INCR
                ("sender_id", 1),  # 发布Feed的用户ID
                ("message_id", 5),  # 文章ID
            ]

            attribute_columns = [('recevice_time', datetime.now().timestamp()), ('read_status', False)]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)
        print(result)
        print(result.is_all_succeed())

        return Response({"message": "ok"})











