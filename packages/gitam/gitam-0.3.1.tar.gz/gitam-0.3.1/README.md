## GITAM

<b>GITAM</b> is a simple, yet elegant, library.


Works only with the [Results Page](https://doeresults.gitam.edu/) for now. New version coming soon!<br>

#### Installing

```python 
$ pip install gitam
```

#### Documentation

```python
>>> from gitam import result
>>> student = result(roll_id=221810309053, semester=6)
>>> student.name
'Rohit G'
>>> student.branch
'Computer Science and Engineering'
>>> student.cgpa
8.68
```

[GLearn](https://login.gitam.edu/), [GParent](https://gparent.gitam.edu/), [Moodle](https://learn.gitam.edu/) etc. will be added soon.