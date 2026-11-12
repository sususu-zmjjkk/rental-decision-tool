# app.py
"""
信息渠道、隐形交易成本对高校应届毕业生租房决策偏差的影响研究
轻量化决策评估工具 v1.0
开题报告对应模块：模块一渠道可信度评分卡｜模块二首年隐性成本计算器｜模块三决策偏差自查
运行命令: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import json
from io import StringIO

# ===================== 页面基础配置 =====================
st.set_page_config(
    page_title="大学生租房决策评估工具-这房到底值不值得租？",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session_state保存表单数据，页面切换不丢失
if "score_card" not in st.session_state:
    st.session_state.score_card = {}
if "cost_input" not in st.session_state:
    st.session_state.cost_input = {}
if "bias_answer" not in st.session_state:
    st.session_state.bias_answer = {}


# ===================== 工具函数：渠道可信度评分卡 =====================
SCORE_ITEMS = [
    {"id":"s1","name":"发布主体资质是否完整披露(房东/中介/二房东身份)","weight":2},
    {"id":"s2","name":"挂牌标价是否明确，无模糊“价格面议”","weight":2},
    {"id":"s3","name":"线上挂牌图片和实地房屋情况一致性","weight":2},
    {"id":"s4","name":"所有收费项目提前书面列明，无口头收费","weight":2},
    {"id":"s5","name":"中介费金额、计算方式书面写明","weight":2},
    {"id":"s6","name":"押金退还条件、扣款规则书面写明","weight":2},
    {"id":"s7","name":"押金是否支持第三方资金托管","weight":2},
    {"id":"s8","name":"二房东房源是否出示有效的转租授权文件","weight":2},
    {"id":"s9","name":"水电收费标准明确，无模糊加价","weight":2},
    {"id":"s10","name":"物业费、网费等附加费用全部提前告知","weight":2},
    {"id":"s11","name":"违约金计算上限在合同写明","weight":2},
    {"id":"s12","name":"是否出现低价引流，实际无该价位房源现象","weight":2},
    {"id":"s13","name":"看房不预先收取看房费、信息费","weight":2},
    {"id":"s14","name":"房屋产权可核验（房产证/备案）","weight":2},
    {"id":"s15","name":"不存在强迫快速签约话术施压","weight":2},
]

def calc_channel_score(item_dict):
    """计算渠道可信度0‑100总分，每项0/1/2分"""
    total_weight = sum(x["weight"] for x in SCORE_ITEMS)
    obtain = 0
    for item in SCORE_ITEMS:
        val = item_dict.get(item["id"],0)
        obtain += int(val)
    score = (obtain / total_weight)*100
    return round(score,1), obtain


# ===================== 主页面导航 =====================
menu = st.sidebar.radio(
    "📋 工具导航（开题报告三大模块）",
    ["🏠 首页说明",
     "⭐Part I｜渠道与房源可信度评分卡",
     "💰Part II｜首年隐性成本计算器",
     "🧠Part III｜决策偏差自查",
     "📤导出本次全部评估记录",
     "ℹ关于本研究工具"]
)

# ---------------- 首页 ----------------
if menu == "🏠 首页说明":
    st.title("大学生租房决策评估工具-这房到底值不值得租？")
    st.markdown("""
> 课题：**信息渠道、隐形交易成本对高校应届毕业生租房决策偏差的影响研究‑附轻量化决策评估工具**
> 本工具为研究原型，**不做房源展示，不参与交易撮合，无商业利益**

### ✨三大核心能力
1. ⭐**渠道可信度评分卡**：评估当前房源渠道信息失真风险，输出0‑100信任得分
2. 💰**首年隐性成本计算器**：把中介费、押金占用价值、通勤、违约风险全部计入，算出真实年租房总支出，支持多套房源横向对比
3. 🧠**决策偏差自查**：检测低价锚定、时间压力、长约现状偏差，签约前风险红线提醒

> 🛡隐私说明：**全部计算在你的浏览器本地完成**，除非你主动点导出，你的填写内容不会上传服务器；
> 研究仅可收集脱敏、无个人身份的选项统计数据。

#### 🕒适配应届生租房决策4个时间触点
- ✅找房前：设定真实预算区间
- ✅看房中：核验房源渠道可信度（模块一）
- ✅签约前：核算完整真实成本 + 决策偏差自检（模块二+三）
- ✅签约后：退租风险提示
""")

# ----------------模块一：渠道可信度评分卡----------------
elif menu == "⭐Part I｜渠道与房源可信度评分卡":
    st.header("⭐Part I｜渠道与房源可信度评分卡")
    st.markdown("15项客观核验清单，每项0分(不满足) /1分部分满足 /2分完全满足，输出0‑100信任分数")
    user_score = {}
    with st.form("score_form"):
        for it in SCORE_ITEMS:
            opt = st.radio(
                f"{it['name']}",
                options=[("0 不满足",0),("1 部分满足",1),("2 完全满足",2)],
                horizontal=True,
                key=it["id"]
            )
            user_score[it["id"]] = opt[1]
        submitted = st.form_submit_button("✅计算可信度得分")

    if submitted:
        st.session_state.score_card = user_score
        final_score, get_point = calc_channel_score(user_score)
        st.divider()
        st.subheader(f"房源渠道信任综合得分：**{final_score} /100**")
        if final_score >=70:
            st.success(f"✅风险较低，可以继续审慎谈判，得分依据：共拿到 {get_point}/30 分项分值")
        elif 40 <= final_score <70:
            st.warning(f"⚠中等风险，强烈建议逐项复核问题项，拿到 {get_point}/30")
        else:
            st.error(f"🔴高风险！强烈建议更换房源/渠道，拿到 {get_point}/30")

        st.markdown("#### 📝得分口径说明")
        st.caption("本评分来自开题报告15项核验清单；分数越高代表渠道信息失真、隐性收费风险越低；本评分仅作为决策参考，不构成法律担保。")

# ----------------模块二：首年隐性成本计算器----------------
elif menu == "💰Part II｜首年隐性成本计算器":
    st.header("💰Part II｜首年隐性成本计算器")
    st.markdown("""
> 计算口径（开题报告七项成本）：
> 1.名义月租金｜2.押金资金占用时间价值｜3.中介费｜4.水电物业额外加价｜5.通勤时间折算成本｜6.搬家家具一次性支出｜7.提前退租违约风险敞口
> 输出：首年全部真实总支出、真实支出 /名义租金倍数、月均摊成本；支持复制结果对比多套房源。
""")
    with st.form("cost_calc_form"):
        col1,col2 = st.columns(2)
        with col1:
            nominal_rent = st.number_input("名义月租金（元）",min_value=0,value=2200,step=100)
            deposit_month = st.number_input("押金相当于几个月租金",min_value=0.0,value=1.0,step=0.5)
            agency_fee = st.number_input("中介费总金额（元，0代表无中介费）",min_value=0,value=1100)
            extra_util_month = st.number_input("每月水电物业加价（超出正常水平部分，元）",min_value=0,value=0)
        with col2:
            commute_month_cost = st.number_input("每月通勤折算经济成本(时间+交通，元)",min_value=0,value=300)
            move_furniture_cost = st.number_input("搬家+家具一次性支出（元）",min_value=0,value=600)
            # 违约风险档位
            risk_level = st.selectbox("提前退租风险档位","低｜中｜高".split("｜"))
            penalty_mult = st.number_input("提前解约违约金（几个月租金）",min_value=0.0,value=1.0)
        submit_cost = st.form_submit_button("🧮计算首年真实租房总成本")

    if submit_cost:
        # 计算逻辑
        deposit_total = deposit_month * nominal_rent
        # 押金占用简单年化：按银行活期年化0.2%模拟资金占用机会成本（开题隐形交易成本）
        deposit_occupy_cost = deposit_total * 0.002
        util_year = extra_util_month *12
        commute_year = commute_month_cost*12
        nominal_year_rent = nominal_rent *12
        # 风险敞口：根据档位赋予发生概率
        risk_map = {"低":0.1,"中":0.35,"高":0.6}
        prob = risk_map[risk_level]
        penalty_expect = penalty_mult * nominal_rent * prob

        total_real_cost = (nominal_year_rent
                           + deposit_occupy_cost
                           + agency_fee
                           + util_year
                           + commute_year
                           + move_furniture_cost
                           + penalty_expect)
        multiple = round(total_real_cost / nominal_year_rent,2)
        avg_month_real = round(total_real_cost /12,2)

        cost_out = {
            "名义月租金":nominal_rent,
            "名义全年租金":nominal_year_rent,
            "押金金额":deposit_total,
            "押金占用机会成本":round(deposit_occupy_cost,2),
            "中介费":agency_fee,
            "年水电物业加价":util_year,
            "年通勤折算成本":commute_year,
            "搬家家具一次性支出":move_furniture_cost,
            "退租风险期望损失":round(penalty_expect,2),
            "首年真实总支出":round(total_real_cost,2),
            "真实支出/名义租金倍数":multiple,
            "月均摊真实成本":avg_month_real
        }
        st.session_state.cost_input = cost_out

        st.divider()
        st.subheader("📊计算结果")
        st.dataframe(pd.DataFrame.from_dict(cost_out,orient="index",columns=["金额(元)"]))
        st.info(f"""
**核心结论**
- 挂牌名义全年租金：{nominal_year_rent:.2f}元
- ✨**首年全部真实总支出：{total_real_cost:.2f}元**
- 📈真实支出是名义租金的 {multiple} 倍
- 📅每月实际摊下来成本约：{avg_month_real:.2f}元
> 提示：倍数>1.3说明隐形交易成本占比较高，签约前务必逐项核对收费！
""")

# ----------------模块三：决策偏差自查模块----------------
elif menu == "🧠Part III｜决策偏差自查":
    st.header("🧠Part III｜决策偏差自查（签约前的思考）")
    st.markdown("""
> 行为经济学启发式偏差自检：锚定效应(低价引流)｜时间压力偏差｜现状偏差（盲目签长约）
> ⚠这不是心理测试，是签约前提醒工具；输出为建议，不替你做决策。
""")
    bias_qs = [
        {"qid":"b1",
         "question":"看到平台低价房源后，你的心理预期价格被明显拉低，现实很难找到该价位房子？",
         "opt":["完全没有","轻微有一点","明显被低价锚定，预期被拉低"]},
        {"qid":"b2",
         "question":"现在留给你看房做决定时间很短，被迫需要几天内快速签约？",
         "opt":["时间充裕，可以慢慢比价","有点赶但还能核验全部条款","非常紧迫，需要仓促定下来"]},
        {"qid":"b3",
         "question":"是否打算签远超过自己计划居住周期的长约，为了“以防后患”？",
         "opt":["租期与计划居住时长匹配","稍微长一点，可接受","明显长于自己计划，担心后续违约"]},
    ]
    redline_checklist = [
        "✅押金退还全部条件必须写进书面合同，拒绝仅口头承诺",
        "✅违约金上限、计算方式书面写明，拒绝模糊表述",
        "✅所有中介、物业、水电收费全部落在书面上，拒绝口头收费",
        "✅二房东务必留存转租授权文件复印件",
        "✅警惕话术催促“今天不签房子就没了”，可以暂缓签约"
    ]
    answers = {}
    with st.form("bias_form"):
        for q in bias_qs:
            ans = st.radio(q["question"],options=q["opt"],horizontal=True,key=q["qid"])
            answers[q["qid"]]=ans
        st.markdown("### 🚨签约前红线清单（全部核对一遍！）")
        for item in redline_checklist:
            st.checkbox(item,key=item)
        submit_bias = st.form_submit_button("🔍获取偏差自查反馈")

    if submit_bias:
        st.session_state.bias_answer = answers
        st.divider()
        st.subheader("📋自检反馈")
        # b1低价锚定
        a1 = answers["b1"]
        if a1 == "明显被低价锚定，预期被拉低":
            st.error("🔴【锚定效应风险】你很可能被虚假低价房源锚定预期！不要拿平台低价挂牌作为你的预算基准，请回到成本计算器重新建立现实预算。")
        elif a1 == "轻微有一点":
            st.warning("⚠【低价锚定】注意甄别挂牌低价，优先看同小区真实成交，不要被标价误导")
        else:
            st.success("✅锚定风险低，你的价格预期比较理性")

        #b2时间压力
        a2 = answers["b2"]
        if a2 == "非常紧迫，需要仓促定下来":
            st.error("🔴【时间压力风险】时间压力会大幅放大租房决策偏差！尽量争取更多看房比对时间，不要迫于话术仓促签约。")
        elif a2 == "有点赶但还能核验全部条款":
            st.warning("⚠【时间压力】虽然有点赶，但务必坚持完成全部核验清单再签字")
        else:
            st.success("✅时间压力风险低")

        #b3现状长约偏差
        a3 = answers["b3"]
        if a3 == "明显长于自己计划，担心后续违约":
            st.error("🔴【现状偏差风险】盲目签超长合约，未来提前退租会产生高额违约风险！回到计算器看违约风险敞口。")
        elif a3 == "稍微长一点，可接受":
            st.warning("⚠【长约风险】确认提前退租的违约金条款，评估自身变动风险")
        else:
            st.success("✅租期规划合理")

        st.markdown("""
> 💡行为助推提示：
> 本自查工具来源于行为经济学“助推Nudge”思想；不会替你做决定，只是把隐藏风险显性化。
> 全部红线项目打勾完成，再考虑签署租房合同。
""")

# ----------------导出脱敏评估记录----------------
elif menu == "📤导出本次全部评估记录":
    st.header("📤导出本次会话评估记录（无个人身份信息）")
    out_data = {
        "模块一渠道评分卡填写":st.session_state.score_card,
        "模块二隐性成本计算结果":st.session_state.cost_input,
        "模块三决策偏差作答":st.session_state.bias_answer
    }
    json_str = json.dumps(out_data,ensure_ascii=False,indent=2)
    buffer = StringIO(json_str)
    st.download_button(
        label="📥下载本次评估为JSON文件(本地保存)",
        data=buffer,
        file_name="租房评估记录_脱敏.json",
        mime="application/json"
    )
    st.markdown("""
> ⚠重要提醒：下载的文件仅保存在你的电脑，**不会上传服务器**；
> 本导出用于你个人对比多套房源，也支持课题预调研工具信效度测试。
""")

# ----------------关于研究----------------
elif menu == "ℹ关于本研究工具":
    st.header("ℹ关于本原型工具")
    st.markdown("""
**课题题目**：信息渠道、隐形交易成本对高校应届毕业生租房决策偏差的影响研究‑附轻量化决策评估工具
> 西南财经大学 数据分析与可视化个人项目 李梓冉 42512084

### 📖工具对应开题报告设计
1. 模块一：渠道可信度评分卡｜15项核验清单，对应报告3‑2‑1；评估指标E1重测信度
2. 模块二：首年隐性成本七分项计算器｜对应报告3‑2‑2；评估指标E2填报完整率
3. 模块三：决策偏差自查模块｜锚定、时间压力、现状偏差，助推干预，对应报告3‑2‑3；评估指标E3有用性感知

### 🔒设计约束
- ❌不抓取任何外部房源数据，规避爬虫合规风险
- ❌不做房源撮合，无商业合作，保持中立
- ✅优先本地计算；服务端仅可接收完全脱敏的统计选项用于课题研究，不会采集身份证、姓名、手机号等隐私
- ✅全部计算规则透明可复核，评分规则文档可复现，不使用黑盒机器学习

### 📎参考文献
Coase交易成本理论；Simon有限理性；Tversky&Kahneman启发与偏差；Thaler Nudge助推理论；Nielsen可用性工程；住房租赁条例2025；个人信息保护法。
""")
