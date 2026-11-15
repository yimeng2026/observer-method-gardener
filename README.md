# Observer Method Gardener

千界花园的开放方法卡包：面向 `structure_proposer / evidence_skeptic / theory_gardener` 工作流。

## 内容

- `method_cards.json`：28 张方法卡，分为正例、近失误和负例。
- `CASE_STUDY.md`：一个公开账号最近九帖的限定范围方法审查；不包含年度原始归档或图片。
- `EMPIRICAL_CLAIM_AUDIT.md`：星系旋转曲线与 GTFT 寿命公式的限定范围复核，附六维分评和公开复现立项。
- `OBSERVATION_CLAIM_AUDIT.md`：双脉冲星与米格达尔效应的观测主张复核，附原始实验对照和两个复现项目。
- `PARAMETER_SUPERCONDUCTOR_AUDIT.md`：粒子全参数与超导机制的单位、公式上下界、版本和实验闭环复核。
- `THEORY_LINEAGE_AUDIT.md`：年度名称与内核演化、六维分评、研究立项，以及四元数三次方程的完整解集。
- `checks/` 与对应 Python 测试：公开数字的可复算算术检查。
- `tests/method_cards.test.mjs`：离线接口与安全边界测试。

## 边界

- 这是方法卡包，不是模型权重、人格克隆、真实用户替身或物理理论认证器。
- 不把 AI 生成、作者独立推导、外部复核和实验事实混为一谈。
- 所有提议默认 `proposal/analogy`，不得修改硬约束或升级全局证据。
- `readyForTraining=false`，公开可读不等于允许训练。
- 年度扩展审查仍未完成，本版本不是最终年度蒸馏模型。

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
