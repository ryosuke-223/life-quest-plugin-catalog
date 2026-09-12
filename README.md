# Life Quest Plugin Catalog

Life Questの公式プラグインカタログです。プラグインはSwiftコードではなく、Life Quest本体の固定判定エンジンが解釈するJSONデータとして登録します。

## ディレクトリ

```text
.
├── catalog.json              # アプリが取得する公開カタログ
├── plugins/                  # 個別プラグインの原本
├── AIRPORT_DATA_SOURCES.md   # 空港プラグインの対象範囲と出典
├── scripts/
│   ├── build_catalog.py      # plugins/*.jsonからcatalog.jsonを生成
│   └── validate_catalog.py   # PR用の形式検証
└── .github/workflows/        # PR検証とGitHub Pages公開
```

## プラグイン追加の流れ

1. `plugins/` に新しいJSONを追加する。
2. `python3 scripts/validate_catalog.py` を実行する。
3. `python3 scripts/build_catalog.py` で `catalog.json` を更新する。
4. [CONTRIBUTING.md](CONTRIBUTING.md)に従い、対象データの出典、ライセンス、更新日をPR本文に記載する。
5. PRを作成し、検証ワークフローが成功した状態でレビューを受ける。
6. `main` にマージするとGitHub Pagesへ公開される。

実データを含むプラグインでは、施設名・位置情報・営業状態などの出典と、再配布可能なライセンスを必ず確認してください。仮データや出典不明のスクレイピングデータは登録しません。

## GitHub Pages設定

リポジトリの Settings → Pages → Build and deployment で、Source を **GitHub Actions** に設定します。

公開後のカタログURLは次の形式です。

```text
https://OWNER.github.io/REPOSITORY/catalog.json
```

このリポジトリの公開URLは
`https://ryosuke-223.github.io/life-quest-plugin-catalog/catalog.json` です。

Life QuestアプリのDebug／Releaseビルドで、Build Settingsの `PLUGIN_CATALOG_URL` にこのURLを設定すると、ユーザーはURLを入力せず、アプリ内の一覧からインストールできます。

## 自動判定の範囲

- `photoLocation`: 写真の撮影位置と項目の座標を固定アダプタで照合
- `healthKitAnnualStepCount`: 現在年のHealthKit歩数を固定アダプタで照合

## 可視化の指定

プラグインは任意のSwiftUIコードを配布できません。`visualizations` には、アプリに組み込まれた固定可視化のタイプと、対象データ・集計方法だけを指定します。これはKibanaのパネル定義に近い方式です。

### 共通ルール

- `visualizations` は省略可能です。省略時はアプリの後方互換デフォルトを使います。
- 同じ `type` は1プラグイン内で1回だけ指定します。
- 可視化の宣言順が詳細画面での表示順になります。
- `showsPeriodSelector` は任意の真偽値です。省略時は `true`（期間選択を表示）として扱います。期間選択を使わないプラグインだけ `false` を指定できます。
- `annualCount` と `cumulativeCount` は項目の `firstVisitYear` を使った初訪問集計です。
- `annualVisitedItemCount` は項目ごとの訪問年履歴を使い、同じ「項目ID × 暦年」を1回として、その年に訪問記録がある項目数を集計します。
- 期間の「すべて」は現在の全状態、「2025年まで」は2025年末時点の累積状態です。
- 年次チャートの `annualCount` は、その年に初訪問した項目数です。
- `cumulativeCount` は、その年までに初訪問した項目数です。
- 年の途中に記録がない年も年軸から省かず、年別値は0、累積値は直前年の値を維持します。記録のない末尾年や現在年は追加しません。
- `completionRate` は、累積訪問項目数 ÷ 全項目数です。
- グループ進捗は初期状態で折りたたみ、展開したときだけ所属項目を表示します。
- `itemList` は詳細画面に全件を並べず、件数と「一覧を見る」導線から専用一覧画面を開きます。長い共通説明は一覧項目ごとに繰り返さず、必要な場合は一覧画面の `?` ヘルプにまとめます。
- `item.detail` は所在地など項目固有の補足に使います。写真位置による自動判定や判定半径は `automation` と `radiusMeters` から共通ヘルプで説明するため、項目詳細に重複して記述しません。

### 対応タイプとパラメータ

| type | 必須・任意パラメータ | 用途 |
| --- | --- | --- |
| `progressSummary` | なし | プラグイン名、説明、全体進捗 |
| `metricCards` | `metrics` | 複数のサマリーメトリクス |
| `lineChart` | `metric`、`aggregation` | 年次推移の線グラフ |
| `barChart` | `metric`、`aggregation` | 年次比較の棒グラフ |
| `areaChart` | `metric`、`aggregation` | 累積・推移の面グラフ |
| `pieChart` | `breakdown` | 状態またはグループの割合 |
| `heatmap` | `dimension` | 年×グループ／年×状態 |
| `achievementCards` | なし | 実績の解除状況 |
| `groupProgress` | なし | `groups` ごとの進捗。グループ必須 |
| `statusMap` | `cluster` | 座標項目の地図。座標項目必須 |
| `statusGrid` | `columns` | 項目状態のグリッド。2〜6列 |
| `nextAchievements` | `limit` | 未解除実績。1〜10件 |
| `itemList` | `sort` | 項目一覧。状態・タイトル・グループ順 |

### 指定できる値

`metricCards.metrics` とチャートの `metric` は次から選びます。

| metric | 意味 |
| --- | --- |
| `visitedCount` | 期間内に訪問済みの項目数 |
| `completionRate` | 期間内の達成率。0〜1を画面でパーセント表示 |
| `remainingCount` | 全項目数から訪問済み項目数を引いた数 |
| `unlockedAchievements` | 期間時点で解除済みの実績数 |
| `totalAchievements` | プラグインに定義された実績数 |

`aggregation` は次の4種類です。

| aggregation | 意味 |
| --- | --- |
| `annualCount` | `firstVisitYear` がその年の項目数。初訪問の年次棒グラフ向け |
| `annualVisitedItemCount` | その年に訪問履歴がある項目数。同一項目・同一暦年は1回。訪問年別の棒グラフ向け |
| `cumulativeCount` | その年以下の `firstVisitYear` を持つ項目数。累積線・エリアグラフ向け |
| `completionRate` | 累積訪問項目数を全項目数で割った値 |

`pieChart.breakdown` は `status`（未訪問・推定・確認済み）または `group`（グループ別）です。`heatmap.dimension` は `yearByGroup`（年×グループの初訪問数）または `yearByStatus`（年までの状態別項目数）です。

### JSON例

```json
"visualizations": [
  {
    "type": "metricCards",
    "metrics": ["visitedCount", "completionRate", "remainingCount"]
  },
  {
    "type": "lineChart",
    "metric": "visitedCount",
    "aggregation": "cumulativeCount"
  },
  {
    "type": "barChart",
    "metric": "visitedCount",
    "aggregation": "annualVisitedItemCount"
  },
  { "type": "groupProgress" },
  { "type": "itemList", "sort": "group" }
],
"showsPeriodSelector": false
```

不明なタイプ・値、重複タイプ、範囲外の列数や件数は、アプリと `scripts/validate_catalog.py` の両方で拒否されます。実行コード、任意のクエリ、任意のSwiftUIを受け付けません。

プラグインから任意のSwiftコード、JavaScript、外部クエリを実行することはできません。
