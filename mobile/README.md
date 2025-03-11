# Blueteeth project development - Mobile

## 架構

```plaintext
mobile/  
│── .dart_tool/  
│── .idea/  
│── android/  
│── build/  
│── ios/  
│── lib/  
│   │── controller/  # 控制器
│   │   │── BookController.dart
│   │   └── UserController.dart
│   │── model/  # 資料模型
│   │   │── Book.dart  
│   │   └── User.dart  
│   │── view/  # UI頁面
│   │   │── BookDetails.dart  
│   │   │── BookSearchPage.dart  
│   │   │── LoginPage.dart  
│   │   │── RegisterPage.dart  
│   │   └── ResultPage.dart  
│   │── config.dart  # 設定檔
│   │── main.dart  # 主程式入口
│   │── router.dart  # 路由設定
│   └── util.dart  # 公用工具
│── .flutter-plugins  
│── .flutter-plugins-dependencies  
│── .gitignore  
│── .metadata  
│── analysis_options.yaml  
│── mobile.iml  
│── pubspec.lock  
│── pubspec.yaml  # Flutter 專案設定
└── README.md  
