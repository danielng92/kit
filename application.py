import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        reload=True,
        port=8000
    )