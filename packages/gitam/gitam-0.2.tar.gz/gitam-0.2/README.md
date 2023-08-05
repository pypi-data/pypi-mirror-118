## GITAM

<b>GITAM</b> is a simple, yet elegant, library.


Works only with the [Results Page](https://doeresults.gitam.edu/) for now. New version coming soon!<br>


#### Installing
<pre>$ pip install gitam</pre>

#### Documentation
<pre><span class="o">&gt;&gt;&gt;</span> <span class="kn">from</span> <span class="nn">gitam</span> <span class="kn">import</span> <span class="nn">Result</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">student</span> <span class="o">=</span> <span class="n">Result</span><span class="p">(</span><span class="s1">221810309053</span><span class="p">)</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">student</span><span class="o">.</span><span class="n">name</span>
<span class="mi">'Rohit G'</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">student</span><span class="o">.</span><span class="n">branch</span>
<span class="mi">'Computer Science and Engineering'</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">student</span><span class="o">.</span><span class="n">cgpa</span>
<span class="mi">8.69</span>
</pre>

<span class="nn">Result</span> uses the GET and POST requests to fetch the data from the [Results Page](https://doeresults.gitam.edu/).

<span class="nn">GLearn</span>, <span class="nn">GParent</span>, <span class="nn">Moodle</span> etc. will be added soon.

<style>
.nn {
    color: #b06;
}
.mi {
    color: #116a1e;
}
.kn {
    color: #002d47;
}
.s1 {
    color: #d52d40;
}
pre {
    font-family: Source Code Pro,monospace;
    background-color: #f9f9f9;
    border: 1px solid #d3d3d3;
    padding: 0 2px 1px;
    font-size: .85rem;
    color: #6c6c6c;
}
</style>