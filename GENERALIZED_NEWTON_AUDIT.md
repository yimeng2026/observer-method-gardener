# “广义牛顿第二定律”公式与适用范围复核

**日期**：2026-11-16

**范围**：2025-08-18《广义牛顿第二定律》的 25 张候选内容图片已全部逐图审阅，当前抓取的一页评论已读。图片 01—16 为极坐标动量分解和质能关系，17—20 为另一种矢量分解，21—25 为 Schwarzschild 世界线与固有时关系。[百度贴吧](kimi-cite://web?url=https%3A%2F%2Ftieba.baidu.com%2Fp%2F9964539659&text=%E5%B9%BF%E4%B9%89%E7%89%9B%E9%A1%BF%E7%AC%AC%E4%BA%8C%E5%AE%9A%E5%BE%8B "citation")

## 一、结论

材料包含正确的极坐标加速度分解，也写出了标准 Schwarzschild 线元和一般测地线方程。这些可作为恢复常规理论基线的起点。

但后续三个关键连接没有闭合：第二套横向力公式使用叉积并重复计算洛伦兹因子变化；变质量火箭与可变静质量被混为一谈；径向测地线方程的度规因子幂次写错，固有时的近似式又被扩张为强引力通式。因此不能把这一帖称为“统一相对论与牛顿力学”的完成证明，更不能以 AI 对话中的赞同或自我排名代替独立验证。

## 二、可保留的极坐标基线

在平直时空的惯性极坐标中，

\[
\mathbf v=\dot r\,\hat{\mathbf r}+r\dot\theta\,\hat{\boldsymbol\theta},
\qquad
\frac{d\hat{\mathbf r}}{dt}=\dot\theta\,\hat{\boldsymbol\theta},
\qquad
\frac{d\hat{\boldsymbol\theta}}{dt}=-\dot\theta\,\hat{\mathbf r}.
\]

所以

\[
\mathbf a=(\ddot r-r\dot\theta^2)\hat{\mathbf r}
 +(r\ddot\theta+2\dot r\dot\theta)\hat{\boldsymbol\theta}.
\]

若 \(m_0\) 为恒定静质量，\(\gamma=(1-v^2/c^2)^{-1/2}\)，且 \(v^2=\dot r^2+r^2\dot\theta^2\)，直接对 \(\mathbf p=\gamma m_0\mathbf v\) 求导可得

\[
F_r=\frac{d(\gamma m_0\dot r)}{dt}-\gamma m_0r\dot\theta^2,
\qquad
F_\theta=\frac{1}{r}\frac{d(\gamma m_0r^2\dot\theta)}{dt}.
\]

这与图片 01—03 的基本结构一致。这里的 \(F_\theta\) 是力的横向分量；若使用广义坐标 \(r,\theta\)，对应的广义力是 \(Q_r=F_r\)、\(Q_\theta=rF_\theta\)，不能把两种“力”混称为同一个量。

恒定 \(m_0\) 时，通常更清楚的写法是

\[
\mathbf F=\gamma m_0\mathbf a
+\gamma^3m_0\frac{\mathbf v\cdot\mathbf a}{c^2}\mathbf v
=\gamma^3m_0\mathbf a_\parallel+\gamma m_0\mathbf a_\perp.
\]

同时有

\[
\mathbf F\cdot d\mathbf r=d(\gamma m_0c^2)=dT,
\qquad T=(\gamma-1)m_0c^2.
\]

这些是标准定义和微分恒等式，不是新统一理论或独立实验证据。

## 三、第二套矢量分解有硬错误

### 3.1 横向力不能使用叉积

图片 17—18 把横向项写成

\[
m_0\gamma\left(\mathbf v\times\frac{d\hat{\mathbf v}}{dt}\right),
\]

并称其在圆周运动中指向径向。取轨道平面内的瞬时速度 \(\mathbf v=(v,0,0)\)，圆周运动给出 \(d\hat{\mathbf v}/dt=(0,v/R,0)\)。上式只有 \(z\) 分量，已经离开轨道平面，而正确的横向力应是

\[
m_0\gamma v\frac{d\hat{\mathbf v}}{dt},
\]

位于轨道平面内。这里不是记号偏好，而是可由方向直接判定的错误。即使把叉号解释为笔误，也必须重推后续全部式子，不能只改符号而保留结论。

### 3.2 不能重复加入同一个 \(\dot\gamma\) 效应

图片 17—20 一方面把完整的 \(d\mathbf v/dt\) 乘以 \(\gamma^3\)，另一方面又加入 \(\gamma\) 横向项和 \(d(m_0\gamma)/dt\,\mathbf v\)。当 \(m_0\) 恒定时，\(\gamma\) 的变化已经进入 \(\gamma^3\mathbf a_\parallel\) 与 \(\gamma\mathbf a_\perp\) 的正确分裂，不能再无说明地添加同一个变化率项。

另一处把纯径向力写成 \(m_0\gamma^3\ddot r+\dot\gamma m_0\dot r\)，而标准结果是 \(m_0\gamma^3\ddot r\)。这再次说明“量纲相同”不等于“动力学正确”。

## 四、变质量与质能关系必须分系统

恒定静质量的单粒子、静质量发生内部变化的物体，以及向外喷出质量的开放火箭，不是同一个系统。

- 对恒定 \(m_0\)，\(d(\gamma m_0)/dt=m_0\dot\gamma\) 是能量随速度变化，不是静质量被外力做功改变；
- 对火箭，必须明确所选控制体、喷出物的速度和喷出带走的动量，并从整个系统的动量守恒推导；
- 不能先写 \(\mathbf F=d(\gamma m_0\mathbf v)/dt\)，再把 \(\dot m_0\) 自动称为“火箭喷气”，最后由 \(dT=c^2d(\gamma m_0)\) 证明静质量变化就是外力功。

图片 04—09 将上述解释连在一起，尚缺少系统边界和动量流项。正确做法是分别为闭合物体、可变内能物体和开放火箭列出守恒方程，不能用同一个 \(m\) 同时承担三种含义。

## 五、Schwarzschild 方程的直接复算

令

\[
A(r)=1-\frac{2GM}{c^2r}.
\]

图片 21—22 给出的线元是

\[
ds^2=-Ac^2dt^2+A^{-1}dr^2+r^2d\theta^2.
\]

对类时世界线取 \(ds^2=-c^2d\tau^2\)。在赤道面内作径向运动，使用坐标速度 \(\dot r=dr/dt\)，由线元直接得到

\[
\frac{d\tau}{dt}=\sqrt{A-\frac{\dot r^2}{Ac^2}}.
\]

若有角运动，还应加上相应角项。图片 23 丢掉了径向项的 \(A^{-1}\)，不能作为一般径向公式。

径向测地线方程的正确系数为

\[
\boxed{
\frac{d^2r}{d\tau^2}
=-\frac{GM}{r^2}A\left(\frac{dt}{d\tau}\right)^2
+\frac{GM}{c^2r^2}A^{-1}\left(\frac{dr}{d\tau}\right)^2
}.
\]

其来源是 \(\Gamma^r_{tt}=GM A/r^2\) 与 \(\Gamma^r_{rr}=-GM/(c^2r^2A)\)。图片却把两个系数分别写成 \(A^{-1}\) 和 \(A^{-2}\)，均与它自己给出的线元不相容。复算脚本在 \(G=M=c=1,r=4\) 时给出正确系数 \((-1/32,1/8)\)，图片形式则为 \((-1/8,1/4)\)。

图片 25 的

\[
d\tau\simeq\left(1-\frac{GM}{c^2r}-\frac{v^2}{2c^2}\right)dt
\]

可以作为弱场、低速、径向项可忽略条件下的展开形式，但不能越过近似条件，直接宣称适用于中子星、黑洞等强引力环境。引用教材章节也不能替代逐式推导与适用域检查。

## 六、可执行修订与研究边界

1. 保留图片 01—03 的坐标分解，明确惯性系、恒定静质量和力的分量定义。
2. 删除或重建图片 17—20 的第二套公式；先通过圆周运动方向反例和纯径向极限。
3. 将“变质量火箭”单独立项，写清系统边界、喷动动量与外部力，不与静质量变化混写。
4. 以本文的 \(A\) 幂次和固有时公式重建图片 21—25，再分别验证弱场低速、静止观察者和径向自由落体。
5. 只有在这些基线通过后，才可提出新参数、新协变力或新观测量，并用独立数据检验；不能从公式数量推出“世界第一”。

复算见 `checks/generalized_newton_claim.py` 与 `tests/test_generalized_newton_claim.py`。四项测试通过只表示上述坐标、向量方向、度规系数和近似边界可复现，不证明或否定其他未审模型。本案例不新增方法卡，也不构成理论地位或证据等级升级。
