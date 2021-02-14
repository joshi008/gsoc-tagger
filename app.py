from flask import Flask, render_template
import csv
import urllib
import os
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
from flask import request


gsocTags = Flask(__name__)
gsocTags.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
gsocTags.config.from_pyfile('settings.py')

# MongoDB will go here i suppose
cluster = MongoClient(gsocTags.config.get("MONGO_URI"))
db = cluster["gsoc"]
collection = db["gsoc-tags"]

tag2020 = ['embedded', 'xpath', 'data analysis', 'react native', 'céu', 'solr', 'ruby', 'jsonnet', 'google web toolkit', 'qemu', 'gtkmm', 'numpy', 'canvas', 'fuzzing', 'twig', 'component-based development', 'qt', 'high performance computing', 'c/c++', 'swig', 'java', 'nodejs', 'postgres', 'gis', 'jupyter notebook', 'go', 'hpx', 'jvm', 'jenkins', 'templates', 'linux', 'ffmpeg', 'sdr', 'grafana', 'service mesh', 'r-project', 'kvm', 'perl', 'win32', 'aws', 'c++11', 'vhdl', 'coq', 'rdf', 'ml', 'chatbots', 'javajava', 'spring', 'javafx', 'swift', 'che', 'nt', 'machine learning', 'velocity', 'vaapi', 'awk', 'bsd unix', 'pallene', 'antlr', 'chapel', 'fonts', 'rails', 'lfe', 'hg', 'ui automation', 'hpc', 'directx', 'jni', 'nlp', 'scheme', 'xen', 'jinja2', 'tcl/tk', 'kotlin', 'networking', 'robotics', 'kubernetes', 'kafka', 'sqlite', 'jakartaee', 'data science', 'ghc', 'homomorphic encryption', 'c99', 'graphite', 'elasticsearch', 'make', 'federated learning', 'linux distribution', 'vue', 'golang', 'web development', 'junit', 'qml', 'concurrency', 'prometheus', 'eclipsejavaide', 'smb', 'gtk', 'css', 'tcl', 'rust', 'unicode', 'xmpp', 'virtualization', 'cython', 'git', 'cmake', 'lunatik', 'svg', 'html5', 'haskell', 'ios', 'symfony', 'arduino', 'tensorflow', 'matlab', 'lua', 'medical imaging', 'c', 'django', 'xml', 'risc-v', 'mysql', 'mobile', 'gcc', 'gradle', 'fortran', 'beam', 'rpc', 'postgresql', 'elixir', 'ruby on rails', 'mongodb', 'secure multi-party computation', 'raspberry pi', 'opencl', 'javascript', 'gnss', 'r', 'x11', 'pygame', 'lwgjl', 'julia', 'pcap', 'cabal', 'openwrt', 'x86', 'ocaml', 'clang', 'c++17', 'mlir', 'bash', 'react', 'codeworld', 'sdl', 'distributed systems', 'bootstrap', 'buildbot', 'vala', 'ros', 'open source databases', 'vulkan', 'gnu autotools', 'tekton', 'webkit', 'wordpress', 'deep learning', 'php', 'docker', 'spinnaker', 'gstreamer', 'cuda', 'cifs', 'mapping', 'shell script', 'fpga', 'python', 'asm', 'unix', 'apis', 'iaccessible2', 'reactnative', 'neo4j', 'cloud', 'html', 'hypervisor', 'space applications', 'python 3', 'cups', 'mariadb', 'scala', 'rest', 'libusb', '.net', 'kibana', 'devops', 'numba', 'webpack', 'linkerd', 'screwdriver', 'bsd make', 'opengl', 'hydra', 'blender', 'posix', 'systemverilog', 'programming-language', 'typescript', 'cpp', 'gnu make', 'dart', 'drones', 'wayland', 'webrtc', 'node.js', 'graphql', 'shell', 'scripting', 'servant', 'game development', 'erlang', 'gazebo', 'flutter', 'vue.js', 'julialang', 'honeypot', 'arm', 'sound open firmware', 'drupal 8', 'electron', 'ci/cd', 'spark', 'rpm', 'win32 api', 'angular', 'sanitizers', 'angularjs', 'c++', 'opencv', 'sql', 'kustomize', 'differential privacy', 'redis', 'terraform', 'libxcam', 'linux kernel', 'ipp', 'assembly', 'asr', 'compiler', 'c#', 'android', 'terminal-kit', 'verilog', 'libuv', 'llvm', 'irc']
tag2020.sort()

tag2019 = ['jenkins', 'squeak', 'ghc', 'singularity', 'protocol buffers', 'aws', 'some/ip', 'wayland', 'prometheus', 'html5 canvas', 'htc vive', 'ui automation', 'ide', 'nodejs', 'ruby', 'bsd unix', 'xml', 'x11', 'raspberry pi', 'gwt', 'c#', 'web development', 'c99', 'selenium', 'vega', 'email', 'nlp', 'distributed systems', 'kubernetes', 'chapel', 'google app engine', 'redis', 'vulkan', 'json', 'lwjgl', 'spir-v', 'c++14', 'c/c++', 'wordpress', 'influxdb', 'servant', 'latex', 'javafx', 'tokio_rs', 'gazebo', 'html', 'spring', 'céu', 'video', 'patroni', 'dlang', 'clojure', 'app engine', 'velocity', 'open-sound-control', 'flask', 'django', 'win32', 'virtualization', 'openapi', 'gtk+', 'jupyter', 'git', 'sdr', 'ionic', 'nss', 'operator', 'mysql', 'tensorflow', 'grpc', 'rest', 'webgl', 'midi', 'c++11', 'r-project', 'ipp', 'swift', 'go', 'skala', 'audio', 'openmp', 'risc-v', 'golang', 'drupal 8', 'fonts', 'cmake', 'vhdl', 'graphite', 'kernel', 'ruby on rails', 'robotics', 'medical imaging', 'web apps', 'rust', 'css', 'smb', 'html5/css3', 'gtk', 'windows', 'fpga', 'containers', 'python 3', 'cabal', 'reactjs', 'xmpp', 'qt5', 'bash', 'swig', 'meteor.js', 'postgres', 'gnss', 'pharo', 'high performance computing', 'vega-lite', 'github', 'web', 'clang', 'openj9', 'perl', 'bsd', 'node.js', 'x86', 'sphinx', 'numba', 'a-frame', 'kconfig', 'qt', 'terraform', 'cakephp', 'html5', 'data analysis', 'sql', 'compilers', 'jsonnet', 'voctomix', 'awk', 'opengl', 'webasssembly', 'elasicsearch', 'opencv', 'component-based development', 'tcl', 'gdscript', 'verilog', 'c++', 'perl6', 'biojs', 'fortran', 'kvm', 'regular expressions', 'cms', 'maps api', 'd3', 'networking', 'elasticsearch', 'jvm', 'yocto', 'codeworld', 'electron', 'lisp', 'documentation', 'opencl', 'php', 'sdl', 'automaton', 'arm', 'asr', 'parallelization', 'mariadb', 'linux', 'symfony', 'osx', 'html/css/js', 'gnu autotools', 'cython', 'angular', 'lua', 'julia', 'open source databases', 'drones', 'asynchronous i/o', 'java', 'llvm', 'sqlite', 'embedded', 'jakarta', 'make', 'shell script', 'grafana', 'c++17', 'unix', 'automotive', 'jinja2', 'gnu make', 'neo4j', 'smalltalk', 'rdbms', 'posix', 'openwrt', 'assembly', 'ios', 'xilinx', 'hg', 'webcomponents', 'machine learning', 'mongodb', 'javascript', 'android', 'search', 'postgresql', 'server', 'typescript', 'gradle', 'assembler', 'operating systems', 'rails', 'unicode', 'linux kernel', 'os', 'nt', 'haskell', 'bazel', 'database', 'compiler', 'gtkmm', 'xen', 'cpp', 'directx', 'shell', 'mpi', 'ai', 'gstreamer', 'scripting', 'arduino', 'boinc', 'r', 'svg', 'html/css', 'docker', 'irc', 'perl5', 'blender', 'jquery', 'isabelle proof assistant', 'c++ libraries c++11 c++14 c++17 c++20', 'deep learning', 'apache spark', 'hardware acceleration', 'cloud', 'scala', 'python', 'cups', 'react native', 'c', 'cuda', 'ansible', 'programming languages', 'iaccessible2', 'gdal', 'win32 api', 'css3', 'bytecode', 'ros', 'ffmpeg', 'angularjs', 'rpc', 'react', 'bootstrap']
tag2019.sort()

tag2018 = ['unreal engine', 'xmpp', 'middleware', 'matlab', 'bsd make', 'hydra', 'linux kernel', 'xpath', 'c++', 'distributed systems', 'gazebo', 'scikit-learn', 'big data', 'symfony', 'meteor.js', 'data analysis', 'cpp', 'python', 'smt', 'cms', 'css3', 'gtk', 'electron', 'machine learning', 'css', 'artificial intelligence', 'fonts', 'r', 'communication protocol', 'gnupg', 'polly', 'opentracing', 'synthesis', 'qemu', 'flask', 'simd', 'spring', 'ffmpeg', 'lua', 'kvm', 'tla+', 'arduino', 'apache kafka', 'graphql', 'tensorflow', 'elasticsearch', 'postgresql', 'rdf', 'opencv', 'ruby on rails', 'd', 'wayland', 'music', 'qml', 'mongodb', 'opengl', 'standards', 'singularity', 'git', 'net', 'nltk', 'javascript/html5/css3', 'php/javascript/html', 'xtext', 'assembly', 'openscenegraph', 'gcc', 'django', 'php', 'compression', 'cloud', 'sockets', 'xia', 'crossplatform', 'webassembly', 'pyth', 'mysql', 'parallelization', 'tcl/tk', 'cython', 'bsd unix', 'grpc', 'javascript', 'javacc', 'xarray', 'cups', 'java', 'd3.js', 'docker', 'webgl', 'object-oriented', 'cad', 'c++17', 'hypervisor', 'c/c++', 'erlang', 'gtk+', 'vim', 'audio', 'golang', 'vhdl', 'prometheus', 'angular', 'webcomponents', 'llvm', 'ocaml', 'reactjs', 'velocity', 'groovy', 'lisp', 'webs', 'robotics', 'ansible', 'posix', 'databases', 'ppcg', 'scilab', 'gnu autotools', 'rails', 'html5', 'scripting', 'browser extension', 'tcp', 'ipp', 'react native', 'node.js', 'video', 'numba', 'jvm', 'postgis', 'python 3', 'computer vision', 'redux', 'ice - zeroc', 'win32', 'hadoop', 'espresso', 'wiki', 'angularjs', 'gobject', 'unix', 'blender', 'isl', 'fsts', 'dpdk', 'directx', 'remote access', 'lxc', 'sparql', 'bash', 'web', 'ddos', 'dask', 'android/ios', 'syntaxnet', 'embedded', 'ceph', 'rspec', 'jupyter', 'haskell', 'hg', 'html5/css3', 'ruby on rail', 'r-project', 'react.js', 'fpga', 'macos', 'elk', 'microservices', 'go', 'html/javascript', 'php/javascript/ajax', 'kubernetes', 'boost', 'ruby', 'rest', 'verilog', 'iot', 'tcl', 'midi', 'advanced data structures', 'physical computing', 'boinc', 'scala', 'isabelle proof assistant', 'cuda', 'c++11', 'content management system', 'opencl', 'rust', 'x11', 'pthon', 'node', 'swig', 'xml', 'jruby', 'asm', 'qt', 'github', 'ios', 'shell script', 'openwrt', 'linux', 'twisted', 'awk', 'cmake', 'mariadb', 'ai', 'lamp', 'yocto', 'xen', 'julia', 'deep learning', 'fortran', 'eclipse', 'spark', 'make', 'sphinx', 'c++14', 'ordbms', 'webkit', 'c', 'sdl', 'gnu make', 'react', 'chisel', 'ros', 'java script', 'frontend', 'svg', 'céu', 'android', 'codecs', 'unicode', 'ionic', 'c#', 'openmp', 'vue.js', 'framework', 'vulkan', 'drones', 'windows', 'rdbms', 'd3', 'datproject', 'bpm', 'web/html/css', 'sql', 'html', 'cakephp', 'dhcp', 'jquery', 'openvpn', 'database', 'json/json-ld', 'web development', 'antlr', 'json', 'cassandra', 'firmware', 'css/html', 'perl', 'hardware acceleration', 'real-time', 'webrtc', 'va-api', 'clojure', 'appengine', 'typescript', 'gnss', 'emberjs', 'swift', 'redis']
tag2018.sort()

def check(string, sub_str): 
    if (string.find(sub_str) == -1): 
        return False 
    else: 
        return True

yeartag = tag2018 + tag2020 + tag2019 

@gsocTags.route('/',methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        year = request.form['year']
        
        tags = request.form.getlist('tags')
        print(year)
        print(tags)
        if(year!=""):
            result = collection.find({"Year":year})
            org = []
            for res in result:
                if( 'all' not in tags):
                    checkc=False
                    for tag in tags:
                        print(res)
                        if(check(res['Tags'], tag)):
                            checkc=True 
                    if(checkc):
                        org.append(res)
                else:
                    org.append(res)
            return render_template('index.html', data=org, tags=yeartag)
        return render_template('index.html',data=[],tags=yeartag)
    else:
        result = collection.find({"Year":"2020"})
        org = []
        for res in result:
            org.append(res)
        return render_template('index.html',data=org,tags=yeartag)

@gsocTags.route('/2020')
def gsoc2020fun():
    result = collection.find({"Year":"2020"})
    org = []
    for res in result:
        org.append(res)
    return render_template('index.html', data=org, tags=tag2020)

@gsocTags.route('/2019')
def gsoc2019fun():
    result = collection.find({"Year":"2019"})
    org = []
    for res in result:
        org.append(res)
    return render_template('index.html', data=org, tags=tag2019)

@gsocTags.route('/2018')
def gsoc2018fun():
    result = collection.find({"Year":"2019"})
    org = []
    for res in result:
        org.append(res)
    return render_template('index.html', data=org, tags=tag2018)

if __name__ == '__main__':
    gsocTags.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    gsocTags.run()