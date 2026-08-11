# Project 3 Corrections

Use this alongside `260327 - project3_api.docx.pdf`.

## Model Path

The PDF assumes:

```text
baseline_model.pkl
```

in the project root. Our Project 2 repo stores it more cleanly at:

```text
project2/models/baseline_model.pkl
```

So Project 3 uses:

```text
models/baseline_model.pkl
```

and `app/model.py` points there.

## FastAPI Startup

The PDF uses:

```python
@app.on_event("startup")
```

That still works in many FastAPI versions, but newer FastAPI recommends lifespan handlers. This starter keeps the code simple and explicit with a startup event because the curriculum is teaching the load-once pattern. If FastAPI shows a deprecation warning, it is not a correctness failure.

## Requirements

The PDF omits `numpy`, but `app/model.py` uses `np.argmax`, so `numpy` is included in `requirements.txt`.

The PDF also installs `uvicorn`, but for local development and Docker reliability this scaffold uses:

```text
uvicorn[standard]
```

## Dockerfile

The PDF copies `baseline_model.pkl` from the root. This project copies:

```dockerfile
COPY models/ ./models/
```

because the model lives under `models/`.

## Tests

The Technology test accepts either `Technology` or `Business`. This is intentional. Project 2 showed that Business and Technology are the most confused pair, so the test should validate service behavior without pretending the classifier is perfect.

## Deployment

Do not deploy until:

- `pytest tests/ -v` passes locally
- `docker build` succeeds
- the Docker container responds on `/health`
- the model file is committed to git

