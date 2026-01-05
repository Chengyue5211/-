# Verify Upgrade  Minimal

## 启动
1) 激活环境：`.venv\Scripts\activate`
2) 启动服务：`uvicorn app.main:app --reload --port 8000`
   或双击 `start_server.bat`

## 核验页
- 打开：`http://127.0.0.1:8000/verify_upgrade/demo-cert`

## 投喂历史知识
- 文档页：`http://127.0.0.1:8000/docs`
- 调用 `POST /api/corpus/register` 注册文本
- 搜索：`GET /api/corpus/search?q=hello`

## 回调模拟
- TSA：`POST /api/tsa/callback`  {"cert_id":"demo-cert","provider":"tsa","status":"success","txid":"0xabc999"}
- CHAIN：`POST /api/chain/callback`  {"cert_id":"demo-cert","provider":"chain","status":"success","txid":"0xdef456"}
