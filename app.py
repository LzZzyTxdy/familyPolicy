from datetime import datetime

import streamlit as st

import CRUD
import pdfOperation as pdf

# 页面标题
st.title("家庭保单小管家")

# 功能选择
function = st.sidebar.selectbox(
    "选择功能",
    (
        "添加家庭成员", "添加保险", "为家人新增保单",
        "输出保单PDF文档", "保存PDF文档", "读取PDF文档",
        "查询保单", "修改保单", "修改保单支付状态", "一键修改所有保单支付状态", "删除保单信息",
        "缴费", "查询缴费记录",
        "提醒缴费", "统计"
    )
)

min_date = datetime(1900, 1, 1)
max_date = datetime.today()

# 功能实现
if function == "添加家庭成员":
    st.subheader("添加家庭成员")

    # 输入家庭成员信息
    name = st.text_input("姓名")
    role = st.text_input("角色")
    birthday = st.date_input("生日", min_value=min_date, max_value=max_date)
    if st.button("添加家庭成员"):
        if not name or not role or not birthday:
            st.error('请输入完整信息')
        else:
            if CRUD.addMember(name, role, str(birthday)):
                st.success("家庭成员添加成功")
            else:
                st.error("家庭成员添加失败")

elif function == "添加保险":
    # 输入保险信息
    company = st.text_input("保险公司")
    product_name = st.text_input("产品名称")
    product_type = st.text_input("产品类型")
    coverage = st.number_input("保额", min_value=0)
    duration = st.number_input("保期", min_value=0, max_value=255)
    payment_time = st.number_input("交费时长", min_value=0)
    if st.button("添加保险"):
        if not company or not product_name or not product_type or not coverage or not duration or not payment_time:
            st.error('请输入完整信息')
        else:
            if CRUD.addInsurance(company, product_name, product_type, coverage, duration, payment_time):
                st.success("保险添加成功")
            else:
                st.error("保险添加失败")

# 关联保单和家庭成员
elif function == "为家人新增保单":
    name = st.text_input("姓名")
    company = st.text_input("保险公司")
    product_name = st.text_input("产品名称")
    warranty_number = st.text_input("保单号")
    effective_date = st.date_input("生效日期")
    premium = st.number_input("保费", min_value=0.0)
    payment_state = st.selectbox("支付状态", ["已支付", "未支付"])
    next_pay_day = st.date_input("下次交费日期")
    period = st.number_input("交费周期（月）", min_value=0)
    state = st.selectbox("状态", ["已生效", "未生效"])

    if payment_state == "已支付":
        payment_state = 1
    else:
        payment_state = 0

    if state == "已生效":
        state = "Active"
    else:
        state = "Ineffective"

    if period == 0:
        period = 'NULL'
        next_pay_day = 'NULL'
    else:
        next_pay_day = f'\'{next_pay_day}\''

    if st.button("关联保单和家庭成员"):
        if not name or not company or not product_name or not warranty_number or not effective_date or not premium:
            st.error('请输入完整信息')
        else:
            if CRUD.addWarranty(name, company, product_name, warranty_number, str(effective_date), premium,
                                payment_state,
                                str(next_pay_day), period, state):
                st.success("保单关联成功")
            else:
                st.error("保单关联失败")

elif function == "输出保单PDF文档":
    st.subheader("输出保单PDF文档")

    name = st.text_input("姓名")
    warranty_number = st.text_input("保单号")
    if st.button("输出某张保单为PDF"):
        if not name or not warranty_number:
            st.error('请输入完整信息')
        else:
            pdf.save_one_warranty_to_pdf(name, warranty_number)
            st.success(f"保单 {warranty_number} 已输出为PDF")

    if st.button("输出所有保单为PDF"):
        if not name:
            st.error('请输入完整信息')
        else:
            pdf.save_all_warranties_to_pdf(name)
            st.success(f"{name} 的所有保单已输出为PDF")

if function == "保存PDF文档":
    st.subheader("保存PDF文档")
    warranty_number = st.text_input("保单号")
    uploaded_file = st.file_uploader("选择一个PDF文件", type=["pdf"])

    if st.button("保存PDF文档"):
        if uploaded_file and warranty_number:
            file_content = uploaded_file.read()
            if pdf.add_one_pdf_to_SQLServer_Content(warranty_number, file_content):
                st.success("添加成功")
            else:
                st.error("添加失败")
        else:
            st.error("请输入正确信息（请确保文件为PDF格式）")

elif function == "读取PDF文档":
    st.subheader("读取PDF文档")
    warranty_number = st.text_input("保单号")
    if st.button("读取PDF文档"):
        if not warranty_number:
            st.error("请输入完整信息")
        else:
            if pdf.read_one_pdf_from_SQLServer(warranty_number):
                st.success("读取成功")
            else:
                st.error("读取失败")

elif function == "查询保单":
    st.subheader("查询保单")

    name = st.text_input("姓名")
    if st.button("查询所有保单"):
        if not name:
            st.error('请输入完整信息')
        else:
            warranties = CRUD.get_all_warranties(name)
            if warranties.empty:
                st.warning("没有找到保单信息")
            else:
                st.dataframe(warranties)

    warranty_number = st.text_input("保单号")
    if st.button("查询某张保单"):
        if not warranty_number:
            st.error('请输入完整信息')
        else:
            warranty = CRUD.get_one_warranty(warranty_number)
            if warranty.empty:
                st.warning("没有找到保单信息")
            else:
                st.dataframe(warranty)

elif function == "修改保单":
    st.subheader("修改保单")
    warrantyNum0 = st.text_input("保单号")
    name = st.text_input("姓名")
    company = st.text_input("保险公司")
    product_name = st.text_input("产品名称")
    effective_date = st.date_input("生效日期")
    premium = st.number_input("保费", min_value=0.0)
    payment_state = st.selectbox("支付状态", ["已支付", "未支付"])
    next_pay_day = st.date_input("下次交费日期")
    period = st.number_input("交费周期（月）", min_value=0)
    state = st.selectbox("状态", ["已生效", "未生效"])

    if payment_state == "已支付":
        payment_state = 1
    else:
        payment_state = 0

    if state == "已生效":
        state = "Active"
    else:
        state = "Ineffective"

    if period == 0:
        period = 'NULL'
        next_pay_day = 'NULL'
    else:
        next_pay_day = f'\'{next_pay_day}\''

    if st.button("修改保单"):
        if (not name or not company or not product_name or not warrantyNum0
                or not effective_date or not premium):
            st.error('请输入完整信息')
        else:
            if (CRUD.updateWarranty(warrantyNum0, name, company, product_name,
                                    str(effective_date), premium,
                                    payment_state,
                                    str(next_pay_day), period, state)):
                st.success("修改成功")
            else:
                st.error("修改失败")

elif function == "修改保单支付状态":
    st.subheader("修改保单支付状态")
    warrantyNum = st.text_input("保单号")
    if st.button("修改保单支付状态"):
        CRUD.update_WARRANTY_state(warrantyNum)
        st.success("修改成功")


elif function == "一键修改所有保单支付状态":
    st.subheader("一键修改所有保单支付状态")
    warrantyNum = CRUD.getWarrantyNum()

    if st.button("修改"):
        for warranty in warrantyNum:
            CRUD.update_WARRANTY_state(warranty)
        st.success("所有保单支付状态修改成功")


elif function == "删除保单信息":
    st.subheader("删除保单信息")
    warranty_number = st.text_input("保单号")
    if st.button("删除保单信息"):
        if not warranty_number:
            st.error('请输入完整信息')
        else:
            if CRUD.deleteWarranty(warranty_number):
                st.success("保单删除成功")
            else:
                st.error("保单删除失败")

elif function == "缴费":
    st.subheader("缴费")
    warranty_number = st.text_input("保单号")
    date = st.date_input("缴费日期")
    tailNum = st.text_input("缴费银行尾号")
    if st.button("缴费"):
        if not warranty_number or not date or not tailNum:
            st.error("请输入完整信息")
        else:
            flag = CRUD.payWarranty(warranty_number, date, tailNum)
            if flag == 2:
                st.error("保单已缴费")
            elif flag == 1:
                st.success("缴费成功")
            elif flag == 3:
                st.success("保单已过最终缴费日期，无需缴费")
            else:
                st.error("保单已失效或已删除")


elif function == "查询缴费记录":
    st.subheader("查询缴费记录")
    warranty_number = st.text_input("保单号")

    if st.button("查询缴费记录"):
        if not warranty_number:
            st.error('请输入完整信息')
        else:
            statistics = CRUD.searchPayment(warranty_number)
            if statistics.empty:
                st.warning("没有缴费信息")
            else:
                st.dataframe(statistics)


elif function == "提醒缴费":
    st.subheader("提醒缴费")

    reminders = CRUD.paymentReminder()
    if reminders.empty:
        st.warning("最近没有需要缴费的保单")
    else:
        st.dataframe(reminders)

elif function == "统计":
    st.subheader("统计")

    statistics = CRUD.countPolicy()
    if statistics.empty:
        st.warning("没有统计信息")
    else:
        st.dataframe(statistics)
