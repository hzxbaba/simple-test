import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="决策动力学模型",
    layout="wide"
)

st.title("决策动力学模型")

questions = [
    {
        "question": "你已经连续忙了很多天，原本计划今晚休息，但一位关系不错的人突然希望你帮他处理一个比较麻烦的问题。",
        "options": {
            "直接拒绝，优先保证自己的状态": {"R": 2, "E": -1},
            "先询问事情严重程度再决定": {"T": 1, "C": 1},
            "即使会影响自己，也倾向于帮忙": {"E": 2, "S": 2},
            "嘴上答应，但内心会明显产生不满": {"E": 1, "C": -1}
        }
    },
    {
        "question": "你负责的一件事情最终失败了，但你认为其中很大一部分原因来自外部环境。",
        "options": {
            "先分析自己哪里还能优化": {"C": 2},
            "认为主要是环境问题，不会过多自责": {"R": 1},
            "会反复回想自己是否本可以避免失败": {"C": 2, "E": 1},
            "会优先寻找责任归属，而不是立刻复盘": {"G": 1}
        }
    },
    {
        "question": "你发现一个机会风险较高，但如果成功，长期收益会非常明显。",
        "options": {
            "更关注失败可能带来的损失": {"R": -2},
            "会先观察别人是否参与": {"G": 1},
            "愿意承担短期波动换长期收益": {"R": 2, "T": 2},
            "会因为不确定性过高而放弃行动": {"R": -1}
        }
    },
    {
        "question": "在一个规则并不明确的新环境中，你通常会：",
        "options": {
            "主动摸索边界并尝试适应": {"R": 1},
            "观察别人怎么做后再行动": {"G": 1},
            "如果没有明确规则，会明显不舒服": {"G": 2},
            "更倾向于自己建立一套行动逻辑": {"S": 1}
        }
    },
    {
        "question": "你与他人的观点出现明显冲突，但公开表达可能影响关系。",
        "options": {
            "直接表达真实想法": {"R": 1, "S": 2},
            "根据场合决定是否表达": {"T": 1},
            "即使不同意，也尽量避免冲突": {"E": 2},
            "表面顺从，但之后会保持距离": {"S": 1}
        }
    },
    {
        "question": "你已经投入大量时间做一件事，但后来发现方向可能错了。",
        "options": {
            "及时停止，重新调整方向": {"T": 2},
            "想再坚持一段时间看看": {"T": 1},
            "很难接受前期投入白费": {"S": 2},
            "会因为不想否定过去的自己而继续": {"S": 3}
        }
    },
    {
        "question": "当别人明显情绪不好时，即使与你无关，你通常会：",
        "options": {
            "不太受影响": {"E": -2},
            "会注意气氛变化，但仍保持原计划": {"E": 0},
            "容易因为对方情绪改变自己的决定": {"E": 2},
            "会主动尝试缓和局面，即使代价是自己让步": {"E": 3}
        }
    },
    {
        "question": "如果一个长期目标短时间内始终没有反馈，你更可能：",
        "options": {
            "继续执行原计划": {"T": 2},
            "调整方法，但目标不变": {"T": 1},
            "怀疑自己是否适合继续": {"E": 1},
            "转向能快速看到结果的事情": {"T": -2}
        }
    },
    {
        "question": "当一个团队效率很低时，你更倾向于：",
        "options": {
            "让大家自行调整": {"G": -1},
            "提出建议，但不过多干涉": {"C": 1},
            "开始频繁介入细节": {"G": 2},
            "更关注为什么没人按预期行动": {"S": 1}
        }
    },
    {
        "question": "如果你发现自己被别人误解了，但解释成本很高。",
        "options": {
            "不解释，接受误解": {"S": -1},
            "只向重要的人解释": {"T": 1},
            "会很在意别人怎么看自己": {"E": 2},
            "即使很累，也希望把事情讲清楚": {"S": 2}
        }
    },
    {
        "question": "你长期处于资源比较紧张的状态时。",
        "options": {
            "优先保护已有资源": {"R": -1},
            "更倾向于建立关系网络": {"E": 1},
            "会提高对风险的敏感度": {"R": -2},
            "开始频繁思考不能再出错了": {"S": 1}
        }
    },
    {
        "question": "面对一个明显能力不如你，但态度强势的人。",
        "options": {
            "无所谓，对结果负责即可": {"E": -1},
            "根据利益决定是否配合": {"T": 1},
            "会因为对方态度产生情绪": {"E": 2},
            "倾向于证明自己是对的": {"S": 2}
        }
    },
    {
        "question": "如果你发现自己对某件事已经失去兴趣，但周围人仍然认可你继续做下去。",
        "options": {
            "停止投入，转向更想做的事情": {"R": 1},
            "维持现状，同时观察机会": {"T": 1},
            "因为已经形成身份标签而难以退出": {"S": 2},
            "担心退出后失去别人认可": {"E": 2}
        }
    },
    {
        "question": "当计划被突然打断时，你通常会：",
        "options": {
            "很快调整状态": {"R": 1},
            "短时间烦躁，但还能继续": {"E": 1},
            "会明显影响后续情绪和效率": {"E": 2},
            "更在意是谁导致计划失控": {"G": 1}
        }
    },
    {
        "question": "如果你发现一段关系长期只消耗你，却很难真正带来价值。",
        "options": {
            "主动降低投入": {"R": 1},
            "保持礼貌但拉开距离": {"T": 1},
            "即使疲惫，也很难彻底切断": {"E": 2},
            "会反复权衡失去这段关系的代价": {"S": 1}
        }
    }
]

scores = {
    "R": 0,
    "T": 0,
    "C": 0,
    "E": 0,
    "G": 0,
    "S": 0
}

answers = []

for i, q in enumerate(questions):

    st.subheader(f"第 {i + 1} 题")

    answer = st.radio(
        q["question"],
        list(q["options"].keys()),
        key=i
    )

    answers.append(answer)

if st.button("生成分析结果"):

    for i, answer in enumerate(answers):

        option_data = questions[i]["options"][answer]

        for key, value in option_data.items():

            scores[key] += value

    normalized_scores = {}

    for key, value in scores.items():

        normalized_scores[key] = max(
            0,
            min(100, 50 + value * 8)
        )

    categories = [
        "风险承受",
        "长期耐受",
        "责任内化",
        "情绪介入",
        "规则依赖",
        "自我一致"
    ]

    values = [
        normalized_scores["R"],
        normalized_scores["T"],
        normalized_scores["C"],
        normalized_scores["E"],
        normalized_scores["G"],
        normalized_scores["S"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("参数结果")

    st.write(f"风险承受: {normalized_scores['R']}")
    st.write(f"长期耐受: {normalized_scores['T']}")
    st.write(f"责任内化: {normalized_scores['C']}")
    st.write(f"情绪介入: {normalized_scores['E']}")
    st.write(f"规则依赖: {normalized_scores['G']}")
    st.write(f"自我一致: {normalized_scores['S']}")

    st.subheader("行为预测")

    if normalized_scores["E"] > 70:
        st.write("高压力环境下，你更容易受到情绪与关系变化影响决策。")

    if normalized_scores["R"] < 40:
        st.write("你对不确定性的容忍度较低，更倾向于降低风险暴露。")

    if normalized_scores["S"] > 70:
        st.write("你对自我叙事的一致性需求较强。")

    if normalized_scores["G"] > 70:
        st.write("规则、秩序与可预测性会显著影响你的安全感。")

    if normalized_scores["T"] > 70:
        st.write("你对长期收益有较高耐受能力。")

    if normalized_scores["C"] > 70:
        st.write("你更容易将问题归因于自身，并倾向于主动修正。")