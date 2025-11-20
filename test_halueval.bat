@echo off
REM Quick test script for HaluEval dataset on Windows

echo ========================================
echo AKGC HaluEval Testing Pipeline
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo Step 1: Downloading HaluEval dataset...
echo ----------------------------------------
python src/download_halueval.py --all --length 100

if %ERRORLEVEL% NEQ 0 (
    echo Error downloading dataset!
    pause
    exit /b 1
)

echo.
echo Step 2: Testing with Standard AKGC...
echo ----------------------------------------
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json

if %ERRORLEVEL% NEQ 0 (
    echo Error testing dataset!
    pause
    exit /b 1
)

echo.
echo Step 3: Testing with Ultra-Optimized AKGC...
echo ----------------------------------------
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --ultra

echo.
echo ========================================
echo Testing Complete!
echo ========================================
echo.
echo Results saved in: results/external/
echo.

pause
