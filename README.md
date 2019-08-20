### Prepare Project1
```bash
mkdir ~/projects cd ~/projects
git clone https://github.com/iFunnyMan520/project1.git
python3.7 -m venv project1 cd project1 
source bin/activate 
pip install -r requirements.txt
```

### Development
```
# Run server on http://localhost:5000/
python server.py

# Run tests
pytest run_tests.py -s -v
```