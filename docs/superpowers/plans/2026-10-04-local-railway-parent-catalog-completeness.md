# ローカル線親カタログ完全性 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 子プラグインの全路線グループが親の会社グループ・路線・`routeLinks` に登録されていることを公開前に検証する。

**Architecture:** 既存の親路線単位の集計とJSON契約は維持する。カタログ検証のクロスマニフェスト検査だけを強化し、子の全路線グループ、親路線、親会社グループが同じ対応関係にあることを検査する。アプリ本体のSwiftコードと公開データの路線項目は変更しない。

**Tech Stack:** Python 3、`unittest`、JSONマニフェスト、GitHub Pages用の生成カタログ。

## Global Constraints

- 親 `local-railways` は経営会社を `groups`、路線を `items` として保持する。
- 子プラグインは1経営会社単位で、駅を `items`、路線を `groups` として保持する。
- 子プラグインの全路線グループは親の `collection.routeLinks` へ1回ずつ登録する。
- 同じ子プラグインのリンク先親路線は、同じ親会社 `groupID` を参照する。
- 子未導入路線の親手動管理は許可する。
- 現在の「リアス線」などの親路線項目は削除しない。
- 既存の `scripts/validate_catalog.py` の未コミット変更を上書きしない。

---

### Task 1: 失敗するクロスマニフェスト検証テストを追加

**Files:**
- Modify: `scripts/test_validate_catalog.py`
- Test data: 既存のテストヘルパーとインラインJSONを使用

**Interfaces:**
- Consumes: `validate_catalog()` の既存エラー報告契約
- Produces: 未リンクの子路線、会社グループ不一致、現在の有効カタログを検査する回帰テスト

- [ ] **Step 1: 既存のcollection検証テストとヘルパーを確認する**

Run: `rg -n "routeLinks|collection|parentPluginID|validate_catalog" scripts/test_validate_catalog.py`

Expected: collectionの有効例と不正例を作る既存パターンを特定する。

- [ ] **Step 2: 未リンク子グループの失敗テストを書く**

子プラグインに2路線グループを置き、親の `routeLinks` に1路線だけ登録したカタログを作る。`validate_catalog()` が `missing parent route link` を含む `ValueError` を送出することを検証する。

- [ ] **Step 3: 子ごとの親会社グループ不一致の失敗テストを書く**

同じ子プラグインの2つの路線リンクを、異なる親 `groupID` の路線へ向けたカタログを作る。`validate_catalog()` が `inconsistent parent group` を含む `ValueError` を送出することを検証する。

- [ ] **Step 4: 失敗を確認する**

Run: `python3 -m unittest scripts.test_validate_catalog`

Expected: 新しい2テストが失敗する。検証実装がまだ不足していることを確認する。

### Task 2: 親子完全性検証を実装

**Files:**
- Modify: `scripts/validate_catalog.py:383-422`

**Interfaces:**
- Consumes: `plugins` の全マニフェスト、既存の `validate_plugin()` 出力
- Produces: 親の各子プラグインに対する完全な路線リンク検証

- [ ] **Step 1: 子路線グループのリンク集合を比較する**

collection検証で、子マニフェストの `groups` ID集合を取得し、対象親の `routeLinks` から `childPluginID` が一致するリンクの `childGroupID` 集合を作る。集合が一致しない場合は、不足または余分なリンクを含むエラーにする。

- [ ] **Step 2: 親路線の会社グループを検証する**

各リンクの `routeID` から親 `items` の `groupID` を取得し、親 `groups` のID集合に含まれることを確認する。同じ子プラグインのリンクで得られた親 `groupID` が複数ある場合は `inconsistent parent group` で拒否する。

- [ ] **Step 3: 実装テストを通す**

Run: `python3 -m unittest scripts.test_validate_catalog`

Expected: Task 1の新規テストを含む全テストがPASSする。

### Task 3: 運用文書を更新

**Files:**
- Modify: `RAILWAY_PLUGIN_DATA_SOURCES.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 2で確定した完全性ルール
- Produces: 子プラグイン追加者が親更新を忘れない手順

- [ ] **Step 1: 鉄道データ出典資料に登録手順を追加する**

子プラグインを追加・更新するとき、1会社の子マニフェスト、親の会社グループ、全路線項目、全 `routeLinks` を同じ変更で更新することを記載する。駅データの追加だけでは公開しないことも明記する。

- [ ] **Step 2: カタログREADMEに検証ルールを追加する**

collectionのクロスマニフェスト検証が、子の全路線グループと親路線・会社グループの対応を確認することを記載する。

### Task 4: 現行カタログと生成物を検証

**Files:**
- Verify: `plugins/local-railways.json`
- Verify: `plugins/railway-sanriku.json`
- Verify: `plugins/railway-tokyo-metro.json`
- Regenerate: `catalog.json`

**Interfaces:**
- Consumes: Task 2の検証処理とTask 3の文書
- Produces: 検証済みで生成物が同期したカタログ

- [ ] **Step 1: 現行カタログの検証を実行する**

Run: `python3 scripts/validate_catalog.py`

Expected: 既存の全マニフェストが検証済みとして終了する。

- [ ] **Step 2: テストスイートを実行する**

Run: `python3 -m unittest discover -s scripts -p 'test_*.py'`

Expected: 全テストがPASSする。

- [ ] **Step 3: 公開カタログを再生成して差分を確認する**

Run: `python3 scripts/build_catalog.py && git diff --exit-code -- catalog.json`

Expected: `catalog.json` に不要な差分がない。

- [ ] **Step 4: 親子対応数を確認する**

Run: `python3 - <<'PY'
import json
from pathlib import Path
root = Path('plugins')
parent = json.loads((root / 'local-railways.json').read_text())
for child_ref in parent['collection']['children']:
    child = json.loads((root / f"{child_ref['pluginID']}.json").read_text())
    linked = {link['childGroupID'] for link in parent['collection']['routeLinks'] if link['childPluginID'] == child['id']}
    assert linked == {group['id'] for group in child['groups']}
print('parent-child railway links are complete')
PY`

Expected: `parent-child railway links are complete` と出力される。

- [ ] **Step 5: 変更をコミットする**

Run: `git add scripts/validate_catalog.py scripts/test_validate_catalog.py RAILWAY_PLUGIN_DATA_SOURCES.md README.md catalog.json && git commit -m "validate complete local railway parent links"`

Expected: 検証コード、テスト、文書、生成カタログが1コミットに記録される。既存の無関係な変更はコミットに含めない。
