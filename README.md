# Life Quest Plugin Catalog

Life Questの公式プラグインカタログです。プラグインはSwiftコードではなく、Life Quest本体の固定判定エンジンが解釈するJSONデータとして登録します。

## ディレクトリ

```text
.
├── catalog.json              # アプリが取得する公開カタログ
├── plugins/                  # 個別プラグインの原本
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

Life QuestアプリのReleaseビルドで、Build Settingsの `PLUGIN_CATALOG_URL` にこのURLを設定すると、ユーザーはURLを入力せず、アプリ内の一覧からインストールできます。

## 自動判定の範囲

- `photoLocation`: 写真の撮影位置と項目の座標を固定アダプタで照合
- `healthKitAnnualStepCount`: 現在年のHealthKit歩数を固定アダプタで照合

プラグインから任意のSwiftコード、JavaScript、外部クエリを実行することはできません。
