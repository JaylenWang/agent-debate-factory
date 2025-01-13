policy_topic = [
    "当今中国大陆，拐卖妇女儿童应该（正）/不应该（反）买卖同罪",
    "征收环保税能（正）/不能（反）有效改善环境污染问题",
    "当今中国大陆，应该（正）/不应该（反）允许商业代孕合法化",
    "董事会性别配额制有助于（正）/无助于（反）实现职场性别平等",
    "发达国家应该（正）/不应该（反）征收“肥胖税”",
    "美国应该（正）/不应该（反）在民间实施禁枪",
    "欧盟新版权法限制二次创作，保护（正）/限制（反）了艺术发展",
    "当前应该（正）/不应该（反）取消房屋预售制度",
    "解决校园暴力更应该依靠法律手段（正）/教育手段（反）",
    "当今中国大陆应该（正）/不应该（反）推行安乐死合法化",
    "当今中国大陆应该（正）/不应该（反）废除死刑"
]

creative_topic = [
    "AI绘画是（正）/不是（反）艺术？",
    "彻底失去记忆后的全新人生应该（正）/不应该（反）对之前犯下的罪行负责？",
    "《朝闻道》中，科学家的挚爱之人应当（正）/不应当（反）阻止其走上真理祭坛？",
    "虐待虚拟游戏的NPC存在（正）/不存在（反）道德问题",
    "如果人工智能发展到帮助人类完成一切工作，这样的生活是可喜的（正）还是可悲的（反）？",
    "如果八十一难的最后一难是吃肉，唐僧应该（正）/不应该（反）拒绝",
    "愚公应该移山（正）/搬家（反）",
    "人一出生时就知道自己的死亡时间可喜（正）/可悲（反）",
    "西天取经让齐天大圣找回自我（正）/失去自我（反）",
    "如果人生是一本小说，角色更重要（正）/情节更重要（反）"
]

fact_topic = [
    "Agent是（正）/不是（反）大模型实现通用人工智能的必经之路",
    "网络社交媒体适合（正）/不适合（反）探讨深刻话题",
    "VAR技术有（正）/没有（反）让足球运动变得更美好",
    "信息碎片化提升（正）/降低（反）了当代人的认知能力",
    "高校奉行“绩点为王”政策对学生成长利大于弊（正）/弊大于利（反）",
    "高考后填志愿应该（正）/不应该（反）以就业为第一考量",
    "举办大型运动赛事对城市的发展利大于弊（正）/弊大于利（反）",
    "科学技术越发展人类越有安全感（正）/没有安全感（反）",
    "食品问题频发，制度缺失（正）/管理缺失（反）是主责",
    "社交媒体对公众舆论的影响利大于弊（正）/社交媒体对公众舆论的影响弊大于利（反）",
    "网络匿名特性有利于（正）/不利于（反）公众议题的讨论",
    "自媒体时代，我们离真相越来越远（正）/越来越近（反）",
    "短视频的火爆是当代人精神文明匮乏（正）/丰富（反）的体现",
    "在当代，数据作为生产要素在全球范围内自由流通利大于弊（正）/弊大于利（反）",
    "现代社会更需要通才（正）/更需要专才（反）"
]

value_topic = [
    "人性本善（正）/人性本恶（反）",
    "金钱是（正）/不是（反）万恶之源",
    "以成败论英雄可取（正）/不可取（反）",
    "美是主观感受（正）/客观存在（反）",
    "正义无非是（正）/不只是（反）利益",
    "顺境（正）/逆境（反）更有利于人的成长",
    "爱使人更自由（正）/更不自由（反）",
    "知易行难（正）/知难行易（反）",
    "现代社会，情理比法理更重要（正）/法理比情理更重要（反）",
    "理想比现实更有意义（正）/现实比理想更有意义（反）",
    "年轻人奋斗的价值体现在过程（正）/体现在结果（反）",
    "以暴制暴是正义（正）/不是正义（反）",
    "温饱是谈道德的必要条件（正）/温饱不是谈道德的必要条件（反）",
    "恶法非法（正）/恶法亦法（反）",
    "无人驾驶汽车遇到危险应乘客保护优先（正）/行人保护优先（反）",
]

TOPICS = policy_topic + creative_topic + fact_topic + value_topic
CANDIDATE_MODEL_LIST = [
    # close
    "google/gemini-pro-1.5",
    "google/gemini-flash-1.5",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20241022",
    "gpt-4o-mini",
    "gpt-4o",
    "glm-4-air",
    # open
    "deepseek-chat",
    "qwen/qwen-2-72b-instruct",
]