# README
Repository for backup application


## アーキテクチャ
<img src="./アーキテクチャ.drawio.svg">


## ベンダーコスト
* API
    * AWS Lambda: *100万request/月 -無料-*
    * AWS Api Gateway REST API: *1万request/0.01USD*
* Object Storage
    * AWS S3: *1GB/0.023USD*
* DB
    * AWS DynamoDB: *25GBデータ -無料-*
* Network
    * AWS CloudFront (CDN): *1,000万request/月 -無料-*
    * お名前.com (Custom Domain): *1500円/年*


## Application URL
https://www.noflexman.tokyo/


## Git Emoji Prefix
🐛  :bug: バグ修正  
👍  :+1: 機能改善  
✨  :sparkles: 部分的な機能追加  
🎨  :art: デザイン変更のみ  
💢  :anger: コンフリクト  
📝  :memo: 文言修正  
♻️  :recycle: リファクタリング  
🔥  :fire: 不要な機能・使われなくなった機能の削除  
💚  :green_heart: テストやCIの修正・改善  
👕  :shirt: Lintエラーの修正やコードスタイルの修正  
🚀  :rocket: パフォーマンス改善  
🆙  :up: 依存パッケージなどのアップデート  
👮  :cop: セキュリティ関連の改善  
⚙   :gear: config変更  
📚  :books: ドキュメント  
