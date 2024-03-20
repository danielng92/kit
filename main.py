import uvicorn


uvicorn.run(
        app="app.main:app",
        reload=True,
        host="0.0.0.0"
    )