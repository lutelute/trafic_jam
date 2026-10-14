# 自然渋滞の実験室

事故も工事も合流もないのに起きる渋滞（自然渋滞）を、運転者を「制御器」とみなした車間追従モデルで動かすデモと、その解説スライドです。

- **デモページ**：https://lutelute.github.io/trafic_jam/
- **発表スライド（20枚）**：https://lutelute.github.io/trafic_jam/slides/ （← → キーでページ送り、N でノート、F で全画面）

内容は次のとおりです。

- **実験1 円形コース**：1周230mに22台（2008年の杉山らの実験と同じ条件）。1台が1回ブレーキを踏むと、減速が後ろへ強まりながら伝わり、止まる車が出て、渋滞のかたまりが後ろへ進みます。
- **実験2 サグ部のある道路**：3kmの1車線の道路に、下り坂から上り坂へ変わる凹部（サグ）があります。来る交通量が上り坂で通れる量を超えると、サグの手前に渋滞がたまります。
- **解説**：モデル化の手順、伝達関数と列安定性（string stability）、ゲイン線図、渋滞吸収車をループに入れたフィルタとして見る見方、サグを「外乱」と「目標の変化」に分けたモデル。

## ファイル

| パス | 内容 |
| --- | --- |
| `index.html` | デモページの元ファイル。Claude の Artifact 用に `<head>` と `<body>` を省いて書いている |
| `tools/build_pages.py` | `index.html` に `<head>` と `<body>` を付けて `docs/index.html` を作る |
| `docs/index.html` | GitHub Pages で配るデモページ（生成物。直接は編集しない） |
| `docs/slides/index.html` | スライドを表示するビューア |
| `docs/slides/deck.json` | スライドの目次 |
| `docs/slides/slides/*.html` | スライド1枚ずつの HTML（1920×1080 の固定キャンバス、Claude の Slides 形式） |

`index.html` を直したら、`python3 tools/build_pages.py` を実行して `docs/index.html` を作り直してください。

## 手元で動かす

```sh
python3 -m http.server 8000 --directory docs
# デモ:     http://localhost:8000/
# スライド: http://localhost:8000/slides/
```

スライドのビューアは `deck.json` と各スライドを読み込むので、ファイルを直接開くのではなく http サーバー経由で開いてください。

## モデル

各車の加速度は FVD モデル（最適速度モデルに相対速度の項を足したもの）で決めます。

```
dv_n/dt = a [ V(s_n) − v_n ] + λ ( v_{n+1} − v_n )
```

`s_n` は前の車との車間、`V(s)` は車間 s のときに出したい速度（S 字の関数）です。`a` は速度を合わせる速さ、`λ` は相対速度への反応です。これに加えて、加減速の上限と、追突を避けるための連続的なブレーキ上限があります。

線形化すると、前の車の速度から自分の速度への伝達関数は次のようになります。

```
G(p) = (λp + aV′) / (p² + (a + λ)p + aV′)
```

列安定性の条件は「すべての ω で |G(jω)| ≤ 1」で、これは V′ ≤ a/2 + λ と同じです。

サグ部では、上り坂で次の二つの項を足しています。

- 勾配の外乱 −(1 − κ)gθ
- 車間の感覚のずれ V(s) → V(s − Δs)

数値は実験を再現したものではなく、しくみを見るためのものです。たとえば渋滞が後ろへ進む速さは、このモデルでは時速約23kmになります。実際の高速道路で報告されている時速15km前後より速めです。

## 参考文献

- Y. Sugiyama et al., New J. Phys. 10, 033001 (2008). https://doi.org/10.1088/1367-2630/10/3/033001
- M. Bando et al., Phys. Rev. E 51, 1035 (1995). https://doi.org/10.1103/PhysRevE.51.1035
- R. Jiang, Q. Wu, Z. Zhu, Phys. Rev. E 64, 017101 (2001). https://doi.org/10.1103/PhysRevE.64.017101
- R. E. Stern et al., Transportation Research Part C 89, 205–221 (2018). https://arxiv.org/abs/1705.01693
- B. Goñi-Ros et al., IET Intelligent Transport Systems 8(5), 499–506 (2014).
- NEXCO東日本「年末年始期間の高速道路渋滞予測について【NEXCO東日本版】」(2023年11月28日)
