# 大数素数计数：精确值、渐近估计与筛法误区复核

**日期**：2026-11-16

**范围**：2025-02-17《谁知道 π(x) 在 x 较大时的真实值？》的两页评论、第 13 楼的 18 条展开回复及 6 张候选内容图片均已审阅。整帖采集范围已经闭合；以下分别判定其中的精确计数、近似公式与证明边界。[百度贴吧](kimi-cite://web?url=https%3A%2F%2Ftieba.baidu.com%2Fp%2F9500700895&text=%E8%B0%81%E7%9F%A5%E9%81%93%CF%80(x)%E5%9C%A8x%E8%BE%83%E5%A4%A7%E6%97%B6%E7%9A%84%E7%9C%9F%E5%AE%9E%E5%80%BC%EF%BC%9F "citation")

## 一、结论

\(\pi(x)\) 是不超过 \(x\) 的素数个数，是逐点确定的整数；\(x/\ln x\)、\(\operatorname{Li}(x)\)、缩放指数积分和 Riemann \(R(x)\) 则是不同的解析表达式或近似工具。它们可以比较定义、误差和计算成本，但不能未经独立精确值就按数值大小排列“谁最准确”。

主帖与展开评论在 \(x=8\times10^{25}\) 时写出的四个数值经高精度复算基本正确；图片中的另一组 \(1.724、1.722、1.721、1.715\times10^{24}\) 均与相应公式不符，不能据此排序。

材料中给出的 \(\pi(10^{25})\approx1.698\times10^{23}\) 也不正确。公开精确值为

\[
\pi(10^{25})=176846309399143769411680.
\]

[arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F1703.08032.pdf&text=The%20computation%20of%20the%20prime%20counting%20function%20%CF%80(x)%20for%20large%20values%20of%20x%20is%20a%20difficult%20problem(the%20latest%20record%20was%20%CF%80(10%5E%7B25%7D)%3D176846309399143769411680%20and%20is%20due%20to%20B%C3%BCthe%2C%20Franke%20and%20Kleinjung%5B4%5D). "citation")

## 二、同一参数下的独立复算

令 \(x=8\times10^{25}\)，使用 70 位十进制精度分别计算，得到：

| 表达式 | 独立复算值 | 对公开材料的判断 |
|---|---:|---|
| \(x/\ln x\) | \(1.3412901151834674\times10^{24}\) | 主帖数值正确；图片的 \(1.715\times10^{24}\) 错误 |
| \(\operatorname{Li}(x)\) | \(1.3645731465572533\times10^{24}\) | 主帖约值正确；图片的 \(1.724\times10^{24}\) 错误 |
| \(e^{-1}\operatorname{Ei}(1+\ln x)\) | \(1.3416808399175136\times10^{24}\) | 主帖约值正确；图片的 \(1.722\times10^{24}\) 错误 |
| Riemann \(R(x)\) | \(1.3645731465570979\times10^{24}\) | 展开评论约值正确；图片的 \(1.721\times10^{24}\) 错误 |

复算见 `checks/prime_counting_estimates.py`，需要 `mpmath`。4 项测试验证这些数值、Legendre 反例、Mertens 前因子及大数输出的非精确值状态。

这里不能从 \(R(x)<\operatorname{Li}(x)\) 推出 \(R(x)\) 离真实 \(\pi(x)\) 更近，因为不知道该点的真实误差符号；也不能把较大的估计值直接当成较好的估计。Riemann \(R(x)\) 本身是光滑近似，不是精确素数计数器。[MathWorld](kimi-cite://web?url=https%3A%2F%2Fmathworld.wolfram.com%2FRiemannPrimeCountingFunction.html&text=The%20Riemann%20prime%20counting%20function%20R(x)%20approximates%20the%20prime%20counting%20function. "citation")

展开评论另称“\(x>6.6\) 时，总有 \(\operatorname{Li}(x)>\pi(x)>x/\ln x\)”。其中左侧的恒成立说法不能保留：Littlewood 已证明 \(\pi(x)-\operatorname{li}(x)\) 会无限次变号，不能把长期数值观察当成全称命题。[MathWorld](kimi-cite://web?url=https%3A%2F%2Fmathworld.wolfram.com%2FRiemannPrimeCountingFunction.html&text=Littlewood%20proved%20in%201914%20that%20pi(x)-li(x)%20changes%20sign%20infinitely%20often%20(Hardy%20and%20Littlewood%201918). "citation")

同理，Riemann 假设 RH 与 Riemann \(R(x)\) 不是同一个对象。即使讨论零点假设对误差界的影响，也不能跳过逐点计算或证明，直接给出巨大 \(x\) 处的精确整数。

## 三、巨大幂次只能标为近似，不能冒充实数精确计数

独立计算的 Riemann \(R\) 近似如下：

| \(x\) | \(R(x)\) 近似值 | 精确 \(\pi(x)\) |
|---|---:|---|
| \(10^{30}\) | \(1.46923988977204327\times10^{28}\) | 本材料未提供 |
| \(10^{50}\) | \(8.76268031750784169\times10^{47}\) | 本材料未提供 |
| \(10^{100}\) | \(4.36197198714070316\times10^{97}\) | 本材料未提供 |
| \(10^{1000}\) | \(4.34483257640119746\times10^{996}\) | 本材料未提供 |

这些值可以回答“某个定义明确的解析近似是多少”，不能回答成“真实素数个数就是多少”。脚本的 `exactPi` 对这些巨大输入保持 `null`，不是计算失败，而是证据类型必须分开。精确值需要可复核的计数算法、运行记录及独立校验，而不是增加小数位数。

展开评论中的 \(10^{10000}\) 示例也能还原为两个不同近似：

\[
\frac{x}{\ln x}\approx4.3429448190325183\times10^{9995},
\qquad
\operatorname{Li}(x)\approx R(x)\approx4.3431334471142686\times10^{9995}.
\]

因此，评论中的 \(4.342944827\times10^{9995}\) 与所谓“官方值” \(4.34313345\times10^{9995}\) 不是两个相互冲突的精确计数，而分别接近 \(x/\ln x\) 和积分型估计。任何“真实值不确定”的说明都不能反过来把这些近似升级为精确值。上述 \(\pi(10^{25})\) 精确值还直接否定了“素数个数多于 \(1.81818181818181818181818\times10^{23}\)”这一下界主张。

## 四、筛法乘积不等于 \(\pi(x)\)

材料先写

\[
\pi(x)=x\prod_{p\le\sqrt x}\left(1-\frac1p\right),
\]

随后改为约等号。等号可以直接用 \(x=25\) 否定：左侧 \(\pi(25)=9\)，右侧却是

\[
25\left(1-\frac12\right)\left(1-\frac13\right)\left(1-\frac15\right)
=\frac{20}{3}\approx6.6667.
\]

正确的 Legendre 公式需要取整、容斥以及小素数修正项。令 \(P\) 为不超过 \(\sqrt x\) 的所有素数乘积，则

\[
\pi(x)=\pi(\sqrt x)-1+\sum_{d\mid P}\mu(d)\left\lfloor\frac{x}{d}\right\rfloor.
\]

在 \(x=25\) 时，容斥部分为

\[
25-12-8-5+4+2+1-0=7,
\]

再加 \(\pi(5)-1=2\)，得到精确值 9。单纯连续乘积丢掉了取整与容斥结构，不能作为精确公式。

即使只把它当渐近估计，也有常数问题。Mertens 定理给出

\[
\prod_{p\le y}\left(1-\frac1p\right)\sim\frac{e^{-\gamma}}{\ln y}.
\]

取 \(y=\sqrt x\)，便有

\[
x\prod_{p\le\sqrt x}\left(1-\frac1p\right)
\sim 2e^{-\gamma}\frac{x}{\ln x},
\qquad 2e^{-\gamma}\approx1.1229189671337703.
\]

所以该乘积与素数定理的 \(x/\ln x\) 之间相差约 12.29% 的渐近前因子，既不是 \(\pi(x)\) 的等价精确式，也不能仅凭“大于某个下界”就宣称最接近真值。[arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F1303.1856&text=%24%24%5Cprod_%7Bp%5Cleq%20x%7D(1-%5Cfrac%7B1%7D%7Bp%7D)%3D%5Cfrac%7Be%5E%7B-%5Cgamma%2BS(x)%7D%7D%7B%5Clog%20x%7D%24%24 "citation")

## 五、不能用“公式趋于无穷”证明孪生素数猜想

评论另称 \(10^n\) 以内孪生素数个数为 \(6^n\)，并以其趋于无穷来支持孪生素数无穷多。这在数值上立即失败：\(n=1\) 时，10 以内只有 \((3,5)\)、\((5,7)\) 两对，并不是 6 对。

更一般地，一个未经验证的公式趋于无穷，不能证明实际对象也有无穷多个。必须先证明公式与真实计数之间的关系，再讨论极限；否则只是把想要证明的结论写进了假设。

## 六、可执行修订

1. 保留主帖与展开评论在 \(8\times10^{25}\) 处的四个正确数值，撤回图片中的错误数值和排序。
2. 将“真实值”“光滑近似”“渐近等价”“有限样本误差”分栏，不混用等号与约等号。
3. 巨大幂次引用近似时写明函数、精度和实现；精确计数必须另附算法与独立校验。
4. 用 Legendre 小样本反例替换朴素筛法乘积的等号，并在渐近讨论中保留 \(2e^{-\gamma}\)。
5. 不以 AI 认可、公式趋于无穷、RH 名称或误差大小排序替代数学证明。

本报告不新增方法卡，不升级任何物理理论或训练证据。整帖材料范围已经闭合；结论只针对其中实际展示的数学命题，不转移为对未审其他帖子的判断。
