import re

import pandas as pd
import pymssql


def connectToSQL(server='Your Server', port='Port Number', user='Your User',
                 password='Your Password', database='Name Of Database'):
    """
    连接数据库，返回游标对象cursor和connect
    :param server: 服务器名称
    :param user: 用户
    :param password: 密码
    :param database: 数据库名称
    :return: 游标对象cursor和connect
    """
    connect = pymssql.connect(server=server, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = connect.cursor()  # 创建一个游标对象cursor，用于执行SQL查询和获取结果
    return cursor, connect


def addMember(name: str, role: str, birthday: str) -> bool:
    """
    增加家庭人员信息
    :param name: 姓名
    :param role: 角色
    :param birthday: 生日
    :return: True:添加成功； False:添加失败
    """
    cursor, connect = connectToSQL()
    sql = f"""INSERT INTO member VALUES('{name}','{role}','{birthday}')"""
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        # print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def deleteMember(name: str) -> bool:
    """
    删除人员信息（注意：只对member进行删除，不涉及其他表，调用时应考虑删除顺序）
    :param name: 姓名
    :return: True:删除成功； False:删除失败
    """
    cursor, connect = connectToSQL()
    sql = f"""DELETE FROM member where name = '{name}';"""
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def updateMember(name: str, name2: str, role2: str, birthday2: str) -> bool:
    """
    更新人员信息
    :param name: 原姓名
    :param name2: 新姓名
    :param role2: 新角色
    :param birthday2: 新生日
    :return: True:更新成功； False:更新失败
    """
    cursor, connect = connectToSQL()
    sql = f"""UPDATE member SET name='{name2}',role='{role2}',birthday='{birthday2}' WHERE name = '{name}';"""
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def searchMember(name: str):
    """
    查找人员信息
    :param name: 姓名
    :return: DataFrame类型信息（姓名，角色，生日）。若查询失败，则return False
    """
    cursor, connect = connectToSQL()
    sql = f"""SELECT* FROM member WHERE name = '{name}';"""
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame(res, columns=columns)
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def addInsurance(company: str, product_name: str, product_type: str, coverage: int, duration: int,
                 payment_time: int) -> bool:
    """
    添加保险
    :param company: 公司
    :param product_name: 产品名称
    :param product_type: 产品类型
    :param coverage: 保额
    :param duration: 期限
    :param payment_time: 交费时长
    :return: True:添加成功; False:添加失败
    """
    cursor, connect = connectToSQL()
    sql = f"""INSERT INTO insurance 
              VALUES('{company}','{product_name}','{product_type}',{coverage},{duration},{payment_time})"""
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def deleteInsurance(company: str, product_name: str) -> bool:
    """
    删除保险，注意：同上，只对保险表做删除操作，不涉及其他表
    :param company: 公司
    :param product_name: 产品名称
    :return: True:删除成功; False:删除失败
    """
    cursor, connect = connectToSQL()
    sql = f"""DELETE FROM insurance WHERE company = '{company}' and product_name = '{product_name}';"""
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def updateInsurance(company0: str, product_name0: str, company: str, product_name: str, product_type: str,
                    coverage: int, duration: int,
                    payment_time: int) -> bool:
    cursor, connect = connectToSQL()
    sql = f"""UPDATE insurance 
              SET company='{company}',product_name='{product_name}',product_type='{product_type}',
              coverage={coverage},duration={duration},payment_time={payment_time}
              WHERE company='{company0}' and product_name='{product_name0}';"""
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def searchInsurance(company: str, product_name: str):
    cursor, connect = connectToSQL()
    sql = f"""SELECT* FROM insurance WHERE company='{company}' and product_name='{product_name}';"""
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame(res, columns=columns)
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def addWarranty(name, company, product_name, warranty_number, effective_date, premium, payment_state, next_pay_day,
                period, state) -> bool:
    cursor, connect = connectToSQL()
    sql = f"""INSERT INTO warranty 
              VALUES({warranty_number},'{effective_date}',
              '{premium}',{payment_state},{next_pay_day},{period},'{state}',
              '{name}','{product_name}','{company}');"""
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def getWarrantyNum():
    cursor, connect = connectToSQL()
    sql = """select warranty_number from warranty;"""
    cursor.execute(sql)
    res = cursor.fetchall()
    warrantyNum = []
    for warranty in res:
        warrantyNum.append(warranty[0])
    return warrantyNum


def deleteWarranty(warrantyNum: str) -> bool:
    """
        仅修改保单为已删除（Deleted）（注意：与dropWarranty进行比较，此函数为逻辑删除）
        :param warrantyNum: 保单号
        :return: 1:删除成功; 0:删除失败
        """
    cursor, connect = connectToSQL()
    if not isDeleted(warrantyNum):
        sql = f"""update warranty
            set state = 'Deleted'
            where warranty_number='{warrantyNum}'"""
        cursor.execute(sql)
        connect.commit()
        cursor.close()
        connect.close()
        return True
    else:
        print(f'保单{warrantyNum}不为生效状态')
        cursor.close()
        connect.close()
        return False


def updateWarranty(warrantyNum0, name, company, productName, effect, premium,
                   paymentState, nextPayday, period, state, ):
    cursor, connect = connectToSQL()
    sql = f"""update warranty
        set effective_date='{effect}',premium={premium},payment_state={paymentState},
        next_pay_day={nextPayday},period={period},state='{state}',name='{name}',product_name='{productName}',company='{company}'
        where warranty_number={warrantyNum0}
    """
    try:
        cursor.execute(sql)
        connect.commit()
        return 1
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        connect.close()


def dropWarranty(warrantyNum: str) -> bool:
    """
    彻底删除保单（同时删除payment表里的有关信息）（注意：与deleteWarranty进行比较，此函数为彻底删除）
    :param warrantyNum: 保单号
    :return: True:删除成功; False:删除失败
    """
    cursor, connect = connectToSQL()
    sql0 = f"""DELETE FROM payment WHERE warranty_number = '{warrantyNum}';"""
    sql1 = f"""DELETE FROM warranty WHERE warranty_number = '{warrantyNum}';"""
    try:
        cursor.execute(sql0)
        connect.commit()
        cursor.execute(sql1)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False


def updatePayment(warrantyNum0, warrantyNum1):
    cursor, connect = connectToSQL()
    sql = f"""update payment
            set warranty_number = {warrantyNum1}
            where warranty_number = {warrantyNum0};
    """
    try:
        cursor.execute(sql)
        connect.commit()
        return 1
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        connect.close()


def updatePDF(warrantyNum0, warrantyNum1):
    cursor, connect = connectToSQL()
    sql = f"""update pdf_
            set warranty_number = {warrantyNum1}
            where warranty_number = {warrantyNum0};
    """
    try:
        cursor.execute(sql)
        connect.commit()
        return 1
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        connect.close()


def isActive(warrantyNum: str) -> bool:
    """
    判断保单是否生效
    :param warrantyNum: 保单号
    :return: 1:生效; 0:失效
    """
    cursor, connect = connectToSQL()
    cursor.execute(f"""select state from warranty where warranty_number='{warrantyNum}';""")
    state = cursor.fetchone()
    if 'Active' == state[0]:
        cursor.close()
        connect.close()
        return True
    else:
        cursor.close()
        connect.close()
        return False


def isLapsed(warrantyNum: str) -> bool:
    """
    判断保单是否失效
    :param warrantyNum: 保单号
    :return: 1:已失效; 0:未失效
    """
    cursor, connect = connectToSQL()
    cursor.execute(f"""select state from warranty where warranty_number='{warrantyNum}';""")
    state = cursor.fetchone()
    if 'Lapse' == state[0]:
        cursor.close()
        connect.close()
        return True
    else:
        cursor.close()
        connect.close()
        return False


def isIneffective(warrantyNum: str) -> bool:
    """
    判断保单是否未生效
    :param warrantyNum: 保单号
    :return: 1:未生效; 0:不为未生效
    """
    cursor, connect = connectToSQL()
    cursor.execute(f"""select state from warranty where warranty_number='{warrantyNum}';""")
    state = cursor.fetchone()
    if 'Ineffective' == state[0]:
        cursor.close()
        connect.close()
        return True
    else:
        cursor.close()
        connect.close()
        return False


def isDeleted(warrantyNum: str) -> bool:
    """
    判断保单是否删除
    :param warrantyNum: 保单号
    :return: 1:已删除; 0:未删除
    """
    cursor, connect = connectToSQL()
    cursor.execute(f"""select state from warranty where warranty_number='{warrantyNum}';""")
    state = cursor.fetchone()
    if 'Deleted' == state[0]:
        cursor.close()
        connect.close()
        return True
    else:
        cursor.close()
        connect.close()
        return False


def isPaid(warrantyNum: str) -> bool:
    """
    判断保单是否已付款
    :param warrantyNum: 保单号
    :return: 1:已付款; 0:未付款
    """
    cursor, connect = connectToSQL()
    cursor.execute(f"""select payment_state from warranty where warranty_number='{warrantyNum}';""")
    payment_state = cursor.fetchone()
    if payment_state[0]:
        cursor.close()
        connect.close()
        return True
    else:
        cursor.close()
        connect.close()
        return False


def get_one_warranty(warrantyNum: str):
    """
    输入姓名和保单id，返回这一张保单的信息(任务书图二)
    :param warrantyNum: 保单号
    :return: DataFrame类型的信息(任务书图二)
    """
    cursor, connect = connectToSQL()
    sql = f"""select m.name, m.role, m.birthday,i.company, i.product_name, w.warranty_number,w.premium, 
	CASE 
		WHEN w.period IS NULL THEN 'Lump sum'
		ELSE CAST(w.period AS NVARCHAR)+' months'
	END as period,(CAST(i.payment_time AS NVARCHAR)+' years')as payment_time, w.effective_date,i.product_type, CAST(i.coverage AS NVARCHAR) AS coverage,
    CASE
		WHEN i.duration = 255 THEN 'Lifelong'
		ELSE CAST(i.duration AS NVARCHAR)+' years'
	END as duration, w.state
    from member as m,insurance as i,warranty as w
    where m.name=w.name and i.product_name=w.product_name and i.company=w.company 
    and w.warranty_number = '{warrantyNum}'
    and (w.state != 'Deleted');
    """
    cursor.execute(sql)
    res = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    connect.close()
    df = pd.DataFrame(res, columns=columns)
    df.index = df.index + 1
    return df


def get_all_warranties(name: str):
    """
    输入姓名，返回DataFrame类型的保单信息
    :param name: 姓名
    :return: DataFrame类型的任务书图1信息(保险类型，保额，保至，公司名称，产品名称，下期交费，交费日，状态(是否生效))
    """
    cursor, connect = connectToSQL()
    sql = f"""select i.product_type,
    CAST(i.coverage AS NVARCHAR) AS coverage,
    CASE 
        WHEN i.duration = 255 THEN 'Lifelong' 
        ELSE CAST(DATEADD(YEAR, i.duration, w.effective_date) AS NVARCHAR) 
    END as finalDate,
    	i.company,i.product_name,
    CASE 
    	WHEN w.payment_state = 1 THEN 'Paid'
    	ELSE CAST(w.premium AS NVARCHAR)
    END as premium,
    CASE 
    	WHEN w.payment_state = 1 THEN '-'
    	ELSE CAST(w.next_pay_day AS NVARCHAR)
    END as nextPayDay,
    	w.state
    from member as m,insurance as i,warranty as w
    where m.name=w.name and i.product_name=w.product_name and i.company=w.company and m.name = '{name}' and (w.state != 'Deleted')
    """
    cursor.execute(sql)
    res = cursor.fetchall()
    # for row in res:
    #     print(row)
    columns = [column[0] for column in cursor.description]
    cursor.close()
    connect.close()
    df = pd.DataFrame(res, columns=columns)
    df.index = df.index + 1
    return df


def add_PAYMENT(warrantyNum: str, tailNum: str) -> bool:
    """
    付款函数
    :param warrantyNum: 保单号
    :param tailNum: 交费银行尾号(后四位)
    :return: 1:添加成功; 0:添加失败
    """
    if not isActive(warrantyNum):
        print('保单已失效')
        return False
    cursor, connect = connectToSQL()
    # 获取保费
    cursor.execute(f"""select CAST(premium AS VARCHAR) from warranty where warranty_number='{warrantyNum}';""")
    fee = cursor.fetchone()
    fee = float(re.findall("\d+\.?\d*", str(fee))[0])  # 正则表达式
    # 插入数据
    sql = f"""insert into payment values('{warrantyNum}',GETDATE(),{fee},'{tailNum}')"""
    try:
        cursor.execute(sql)
        connect.commit()
        update_WARRANTY_payment_state_to_1(warrantyNum)
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def update_WARRANTY_payment_state_to_1(warrantyNum: str) -> bool:
    """
    更新保单表支付状态为1（已支付），返回是否更改成功
    :param warrantyNum: 保单号
    :return: 1:更改成功; 0:更改失败
    """
    cursor, connect = connectToSQL()
    if not isActive(warrantyNum):
        print(f'保单{warrantyNum}已失效')
        return False
    if isPaid(warrantyNum):
        print(f'保单{warrantyNum}已付款')
        return False
    sql = f"""UPDATE warranty
        SET payment_state = 1
        WHERE warranty_number='{warrantyNum}'"""
    cursor.execute(sql)
    connect.commit()

    cursor.close()
    connect.close()
    return True


def update_WARRANTY_payment_state_to_0(warrantyNum: str) -> bool:
    """
    更新保单表支付状态为0（未支付），返回是否更改成功
    :param warrantyNum: 保单号
    :return: 1:更改成功; 0:更改失败
    """
    cursor, connect = connectToSQL()
    if not isActive(warrantyNum):
        print(f'保单{warrantyNum}已失效')
        return False
    if not isPaid(warrantyNum):
        print(f'保单{warrantyNum}未付款')
        return False
    sql = f"""UPDATE warranty
        SET payment_state = 0
        WHERE warranty_number='{warrantyNum}'"""
    cursor.execute(sql)
    connect.commit()

    cursor.close()
    connect.close()
    return True


def update_WARRANTY_state_to_Active(warranty: str) -> bool:
    """
    仅修改保单为生效中（似乎没什么用）
    :param warranty: 保单号
    :return: 1:更改成功; 0:更改失败
    """
    cursor, connect = connectToSQL()
    if not isActive(warranty):
        sql = f"""update warranty
        set state = 'Active'
        where warranty_number='{warranty}'"""
        cursor.execute(sql)
        connect.commit()

        cursor.close()
        connect.close()
        return True
    else:
        print(f'保单{warranty}生效中')
        cursor.close()
        connect.close()
        return False


def update_WARRANTY_state_to_Ineffective(warranty: str) -> bool:
    """
    仅修改保单为仍未生效（未到生效日期）
    :param warranty: 保单号
    :return: 1:更改成功; 0:更改失败
    """
    cursor, connect = connectToSQL()
    if not isActive(warranty):
        sql = f"""update warranty
        set state = 'Ineffective'
        where warranty_number='{warranty}'"""
        cursor.execute(sql)
        connect.commit()

        cursor.close()
        connect.close()
        return True
    else:
        print(f'保单{warranty}生效中')
        cursor.close()
        connect.close()
        return False


def update_WARRANTY_state_to_Lapse(warranty: str) -> bool:
    """
    仅修改保单为已失效（Lapse）
    :param warranty: 保单号
    :return: 1:更改成功; 0:更改失败
    """
    cursor, connect = connectToSQL()
    if isActive(warranty):
        sql = f"""update warranty
        set state = 'Lapse'
        where warranty_number='{warranty}'"""
        cursor.execute(sql)
        connect.commit()
        cursor.close()
        connect.close()
        return True
    else:
        print(f'保单{warranty}已失效')
        cursor.close()
        connect.close()
        return False


def isExpired(warrantyNum: str) -> bool:
    """
    保单是否到期
    :param warrantyNum: 保单号
    :return: 1:到期; 0:未到期
    """
    cursor, connect = connectToSQL()
    sql = f"""
    select
	CASE
		WHEN finalDate = 'Lifelong' or cast(GETDATE() as date)<finalDate THEN 0
		ELSE 1
	END as isExpire
from (select
    CASE 
        WHEN i.duration = 255 THEN 'Lifelong' 
        ELSE CAST(DATEADD(YEAR, i.duration, w.effective_date) AS NVARCHAR) 
    END as finalDate
    from member as m,insurance as i,warranty as w
    where m.name=w.name and i.product_name=w.product_name and i.company=w.company
	and warranty_number='{warrantyNum}') as finalDate;"""
    cursor.execute(sql)
    flag = cursor.fetchone()
    cursor.close()
    connect.close()
    return flag[0]


def isReachingNextPayDay(warrantyNum: str) -> bool:
    """
    今天是否到付款截止日期（注意：1.未检测保单是否仍生效，2.保期为1年的保单返回未到期(False)）
    :param warrantyNum: 保单号
    :return: 1:到期; 0:未到期
    """
    cursor, connect = connectToSQL()
    sql = f"""select
	CASE
		WHEN (cast(GETDATE() as date) >= next_pay_day) THEN 1
		ELSE 0
	END as isReachingNextPayDay
from (select next_pay_day 
		from warranty 
		where warranty_number='{warrantyNum}') as next_pay_day;"""
    cursor.execute(sql)
    flag = cursor.fetchone()
    cursor.close()
    connect.close()
    return flag[0]


def isReachingEffectiveDay(warrantyNum: str) -> bool:
    """
    今天是否到保单生效日期
    :param warrantyNum: 保单号
    :return: 1:到生效日期; 0:未到生效日期
    """
    cursor, connect = connectToSQL()
    sql = f"""select
	CASE
		WHEN (cast(GETDATE() as date) >= effective_date) THEN 1
		ELSE 0
	END as isReachingEffectiveDay
from (select effective_date 
		from warranty 
		where warranty_number='{warrantyNum}') as effective_date;"""
    cursor.execute(sql)
    flag = cursor.fetchone()
    # print(flag)
    cursor.close()
    connect.close()
    return flag[0]


def isReachingLastPayDay(warrantyNum: str) -> bool:
    """
    今天是否到保单最后的付款日期
    :param warrantyNum: 保单号
    :return: 1:到最后的付款日期; 0:未到最后的付款日期
    """
    cursor, connect = connectToSQL()
    sql = f"""select 
	CASE
		WHEN (cast(GETDATE() as date) >= lastPayDay) THEN 1
		ELSE 0
	END as isReachingLastPayDay
from(
select CAST(DATEADD(YEAR,i.payment_time,w.effective_date) as date) as lastPayDay
from insurance as i,warranty as w
where i.product_name=w.product_name and i.company=w.company and 
	(w.state != 'Deleted') and w.warranty_number='{warrantyNum}'
) as lastPayDay;"""
    cursor.execute(sql)
    flag = cursor.fetchone()
    # print(flag)
    cursor.close()
    connect.close()
    return flag[0]


def getPaymentState(warrantyNum: str) -> bool:
    """
    获取支付状态
    :param warrantyNum: 保单号
    :return: True:已支付; False:未支付
    """
    cursor, connect = connectToSQL()
    sql = f"""select payment_state from warranty where warranty_number='{warrantyNum}';"""
    cursor.execute(sql)
    payment_state = cursor.fetchone()
    cursor.close()
    connect.close()
    return payment_state[0]


def update_NEXT_PAY_DATE_to_NULL(warrantyNum: str) -> bool:
    cursor, connect = connectToSQL()
    sql = f"""UPDATE warranty SET next_pay_day = NULL where warranty_number='{warrantyNum}';"""
    try:
        cursor.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connect.close()


def update_Premium_to_0(warrantyNum: str) -> bool:
    cursor, connect = connectToSQL()
    sql = f"""UPDATE warranty SET premium = 0 where warranty_number='{warrantyNum}';"""
    try:
        cursor.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connect.close()


def update_WARRANTY_state(warrantyNum: str) -> None:
    """
    每天对每张保单执行该函数，即可修改保单信息（payment_state(仅从1修改为0，0->1见函数update_WARRANTY_payment_state_to_1), next_pay_day, state）
    :param warrantyNum: 保单号
    :return: True:成功修改; False:未修改
    """
    cursor, connect = connectToSQL()

    # 若保单到期，则修改为失效
    if isExpired(warrantyNum):
        update_WARRANTY_state_to_Lapse(warrantyNum)
        cursor.close()
        connect.close()
        return True

    # 若保单未生效，则无需修改
    if not isReachingEffectiveDay(warrantyNum):  # 今天没到生效日
        print(f'保单{warrantyNum}未到生效日期，无需修改')
        cursor.close()
        connect.close()
        return False
    else:  # 今天保单开始生效
        update_WARRANTY_state_to_Active(warrantyNum)

    # 若保单不为生效状态（失效/已删除），则无需修改
    if not isActive(warrantyNum):
        print(f'保单{warrantyNum}已失效，无法修改')
        cursor.close()
        connect.close()
        return False

    # 接下来保单为生效状态

    # 已经过了缴费时间
    if isReachingLastPayDay(warrantyNum):
        update_WARRANTY_payment_state_to_1(warrantyNum)
        update_NEXT_PAY_DATE_to_NULL(warrantyNum)  # 接下来没有next_pay_day了
        update_Premium_to_0(warrantyNum)  # 接下来保费为0，在统计时不会加上去
        return True
    else:  # 还在缴费时间里
        pass

    # 保单生效的情况下：
    if getPaymentState(warrantyNum):  # 已支付
        if not isReachingNextPayDay(warrantyNum):  # 未到付款截至日期
            print('保单生效，已付款，未到付款截止日期')
            cursor.close()
            connect.close()
            return False
        else:  # 今天为付款截至日期
            update_WARRANTY_payment_state_to_0(warrantyNum)
            update_WARRANTY_next_pay_day(warrantyNum)
            cursor.close()
            connect.close()
            return True
    else:  # 未支付
        if not isReachingNextPayDay(warrantyNum):  # 未到付款截至日期
            print('保单生效，未付款，未到付款截止日期')
            cursor.close()
            connect.close()
            return False
        else:  # 今天为付款截至日期
            update_WARRANTY_state_to_Lapse(warrantyNum)
            cursor.close()
            connect.close()
            return True


def update_WARRANTY_next_pay_day(warrantyNum: str) -> bool:
    """
    修改交费截止日期（注意：没有任何检测）
    :param warrantyNum: 保单号
    :return: 1:已修改; 0:未修改
    """
    # if not isActive(warrantyNum):
    #     print(f'保单{warrantyNum}已失效')
    #     return False
    # if not isPaid(warrantyNum):
    #     print(f'保单{warrantyNum}未付款')
    #     return False

    cursor, connect = connectToSQL()
    sql = f"""select next_pay_day,period from warranty where warranty_number='{warrantyNum}';"""
    cursor.execute(sql)
    res = cursor.fetchall()
    date = res[0][0]
    period = res[0][1]
    if res[0][0] is None:
        print(f'该保单{warrantyNum}保费一次性交清')
        cursor.close()
        connect.close()
        return False
    else:
        update = f"""update warranty
                     set next_pay_day = DATEADD(MONTH,{period},'{date}')
                     where warranty_number='{warrantyNum}'"""
        cursor.execute(update)
        connect.commit()
        cursor.close()
        connect.close()
        return True


def paymentReminder():
    """
    提醒交费
    :return: 保单信息（DataFrame类型）
    """
    cursor, connect = connectToSQL()
    sql = """SELECT name,warranty_number,company,product_name,next_pay_day,premium 
             FROM warranty 
             WHERE (next_pay_day BETWEEN GETDATE() AND DATEADD(MONTH,1,GETDATE())) and 
                    payment_state = 0 and
                    (state = 'Active' or state = 'Ineffective');"""
    cursor.execute(sql)
    res = cursor.fetchall()

    if not res:
        sql = """SELECT TOP 3 name,warranty_number,company,product_name,next_pay_day,premium
                 FROM warranty 
                 WHERE next_pay_day IS NOT NULL and (state = 'Active' or state = 'Ineffective') and payment_state = 0
                 ORDER BY next_pay_day ASC;"""
        cursor.execute(sql)
        res = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    # columns=['姓名','保单号','公司','产品名称','缴费截止日期','保费']
    cursor.close()
    connect.close()
    df = pd.DataFrame(res, columns=columns)
    df.index = df.index + 1
    return df


def countPolicy():
    """
    统计每个人这一年内的保单信息（功能7）
    :return: DataFrame类型数据（姓名，保单数量，保额，保费）
    """
    cursor, connect = connectToSQL()

    sql = """select m.name,count(warranty_number) as nums,sum(coverage) as coverage,sum(premium) as premium
             from member as m,insurance as i,warranty as w
             where m.name=w.name and i.product_name=w.product_name and i.company=w.company and w.state = 'Active'
             group by m.name;"""
    cursor.execute(sql)
    res = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    sql1 = """with tmp as
(select m.name,count(warranty_number) as nums,sum(coverage) as coverage,sum(premium) as premium
from member as m,insurance as i,warranty as w
where m.name=w.name and i.product_name=w.product_name and i.company=w.company and w.state = 'Active'
group by m.name)
    select 'sum'as name,sum(nums) as nums, sum(coverage) as coverage, sum(premium) as premium from tmp
    """
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    columns1 = [column[0] for column in cursor.description]

    cursor.close()
    connect.close()
    df = pd.DataFrame(res, columns=columns)
    df1 = pd.DataFrame(res1, columns=columns1)
    df = df._append(df1, ignore_index=True)
    df.index = df.index + 1
    return df


def searchPayment(warrantyNum: str):
    """
    获取保单支付信息
    :param warranty: 保单号
    :return:
    """
    cursor, connect = connectToSQL()
    sql = f"""select * from payment where warranty_number = '{warrantyNum}'"""
    cursor.execute(sql)
    res = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    df = pd.DataFrame(res, columns=columns)
    df.index = df.index + 1
    return df


def payWarranty(warrantyNum: str, date, tailNum) -> int:
    """
    支付保单
    :param warrantyNum: 保单号
    :return: True:缴费成功；False:缴费失败
    """
    cursor, connect = connectToSQL()

    if isActive(warrantyNum) or isIneffective(warrantyNum):
        if isPaid(warrantyNum):
            print('保单已付款')
            return 2
        elif isReachingLastPayDay(warrantyNum):
            print('已过最终缴费日期')
            return 3
        else:
            sql = f"""select premium from warranty where warranty_number='{warrantyNum}';"""
            cursor.execute(sql)
            res = cursor.fetchone()
            sql1 = f"""insert into payment values({warrantyNum},'{date}',{res[0]},{tailNum})"""
            cursor.execute(sql1)
            connect.commit()
            update_WARRANTY_payment_state_to_1(warrantyNum)
            return 1
    else:
        print('保单已失效或已删除')
        return 0


if __name__ == '__main__':
    connectToSQL()
    print('ok')
