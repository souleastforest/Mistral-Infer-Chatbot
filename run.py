import uvicorn
uvicorn.run("codestral_mamba.fastapi_server:app", host="0.0.0.0", port=18000)