# Observer Method Gardener

千界花园的开放方法卡包：面向 `structure_proposer / evidence_skeptic / theory_gardener` 工作流。

## 内容

- `method_cards.json`：49 张方法卡，分为正例、近失误和负例。
- `CASE_STUDY.md`：一个公开账号最近九帖的限定范围方法审查；不包含年度原始归档或图片。
- `EMPIRICAL_CLAIM_AUDIT.md`：星系旋转曲线与 GTFT 寿命公式的限定范围复核，附六维分评和公开复现立项。
- `OBSERVATION_CLAIM_AUDIT.md`：双脉冲星与米格达尔效应的观测主张复核，附原始实验对照和两个复现项目。
- `PARAMETER_SUPERCONDUCTOR_AUDIT.md`：粒子全参数与超导机制的单位、公式上下界、版本和实验闭环复核。
- `THEORY_LINEAGE_AUDIT.md`：年度名称与内核演化、六维分评、研究立项，以及四元数三次方程的完整解集。
- `SOLAR_CORONA_CLAIM_AUDIT.md`：日冕加热、日震统计、太阳中微子、卫星计时与多体分类的 150 图专项复核。
- `SIX_FORCE_ENGINEERING_AUDIT.md`：室温超导、同位素对照、聚变、真空能、通信与工程路线图的 140 图专项复核。
- `IDEAL_NONCRYSTAL_MAPPING_AUDIT.md`：真实理想非晶体研究、参数映射、合金与工程扩张的 108 图专项复核。
- `MASS_ENERGY_DERIVATION_AUDIT.md`：质能关系的循环定义风险、曲率抵消假设与氘氚参考能量的 36 图专项复核。
- `GOLDBACH_ESTIMATE_AUDIT.md`：两篇哥德巴赫帖的 18 图审阅、独立素数枚举、Li 口径与留出样本复算。
- `HARMONIC_APPROXIMATION_AUDIT.md`：两则调和级数材料的 10 图审阅、展开系数、精确有限和与 ζ(1) 极点复核。
- `NS_FOLLOWUP_SCOPE_AUDIT.md`：NS 后续帖的 96 图审阅、命题范围、陈数量子化与形式证明边界。
- `NS_ANALYTICAL_CLAIM_AUDIT.md`：NS 精准解析帖的 17 图审阅、槽道流算例、模拟评审与一般证明边界。
- `NEW_OFFICIAL_SCIENCE_AUDIT.md`：新官科研究准则、四参数版本、引力子与暗物质数值的 13 图专项复核。
- `CROSS_DOMAIN_APPLICATION_AUDIT.md`：拓扑病理学与治沙方案的跨学科准入、风险边界和退出条件。
- `MESON_PREDICTION_AUDIT.md`：介子全论的公开质疑、参数来源、算子和 \(B_c(2S)\) 历史观测核查。
- `prediction_registry.py`、`prediction_registry.json`：8 条定量预言及其来源、历史观测、核查状态和修订义务。
- `PROJECT_PORTFOLIO.md`：全部已有成果、研究项目状态、优先顺序和停止条件的统一总表。
- `theory_diff.py`、`records/`：机器可读的理论语义差异账本，现有 FEQ→GTFT、GTFT→DSF 和 CNF 旧版→整改版三份记录。
- `VISUAL_REVIEW_COVERAGE.json`：跨全部当前审查范围登记 34 帖、1028 张图片；只含编号和哈希，不公开原始图片。
- `ANNUAL_COVERAGE.json`：年度 532 篇的采集、评论和图片保存门禁快照；不含原帖或图片。
- `checks/` 与对应 Python 测试：公开数字的可复算算术检查。
- `tests/method_cards.test.mjs`：离线接口与安全边界测试。

## 边界

- 这是方法卡包，不是模型权重、人格克隆、真实用户替身或物理理论认证器。
- 不把 AI 生成、作者独立推导、外部复核和实验事实混为一谈。
- 所有提议默认 `proposal/analogy`，不得修改硬约束或升级全局证据。
- `readyForTraining=false`，公开可读不等于允许训练。
- 年度代表案例总评已定稿；全图语义审阅尚未完成，本版本不是最终年度蒸馏模型。

## 花园接口

把相关卡片的 `cardId / ruleText / applicability` 传给 `proposeIntuitionWithModel({ methodCards })`。花园单次接受 **1—20 张**；应根据任务选用少量相关卡片，跨批次审查时逐批调用，不通过放宽上限一次性注入全部卡片。

## 离线验证

需要本机存在千界花园对应实现。将 `GARDEN_ROOT` 设为花园项目根目录，然后运行：

```bash
npx --yes bun test tests/method_cards.test.mjs
```

测试使用合成回复，不发起付费模型调用。它验证接口兼容与安全边界，不证明科学能力或预测正确率。

## 来源与许可

方法卡是本项目对公开材料的抽象方法总结，不包含原文归档。公开来源链接保留在卡片中；没有据此推断训练许可。项目尚未给外部来源材料授予或声称任何额外许可。
