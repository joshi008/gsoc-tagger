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

tag2020 = ['.net', 'android', 'angular', 'angularjs', 'antlr', 'apis', 'arduino', 'arm', 'asm', 'asr', 'assembly', 'awk', 'aws', 'bash', 'beam', 'blender', 'bootstrap', 'bsd make', 'bsd unix', 'buildbot', 'c', 'c#', 'c++', 'c++11', 'c++17', 'c/c++', 'c99', 'cabal', 'canvas', 'chapel', 'chatbots', 'che', 'ci/cd', 'cifs', 'clang', 'cloud', 'cmake', 'codeworld', 'compiler', 'component-based development', 'concurrency', 'coq', 'cpp', 'css', 'cuda', 'cups', 'cython', 'c�u', 'dart', 'data analysis', 'data science', 'deep learning', 'devops', 'differential privacy', 'directx', 'distributed systems', 'django', 'docker', 'drones', 'drupal 8', 'eclipsejavaide', 'elasticsearch', 'electron', 'elixir', 'embedded', 'erlang', 'federated learning', 'ffmpeg', 'flutter', 'fonts', 'fortran', 'fpga', 'fuzzing', 'game development', 'gazebo', 'gcc', 'ghc', 'gis', 'git', 'gnss', 'gnu autotools', 'gnu make', 'go', 'golang', 'google web toolkit', 'gradle', 'grafana', 'graphite', 'graphql', 'gstreamer', 'gtk', 'gtkmm', 'haskell', 'hg', 'high performance computing', 'homomorphic encryption', 'honeypot', 'hpc', 'hpx', 'html', 'html5', 'hydra', 'hypervisor', 'iaccessible2', 'ios', 'ipp', 'irc', 'jakartaee', 'java', 'javafx', 'javajava', 'javascript', 'jenkins', 'jinja2', 'jni', 'jsonnet', 'julia', 'julialang', 'junit', 'jupyter notebook', 'jvm', 'kafka', 'kibana', 'kotlin', 'kubernetes', 'kustomize', 'kvm', 'lfe', 'libusb',
           'libuv', 'libxcam', 'linkerd', 'linux', 'linux distribution', 'linux kernel', 'llvm', 'lua', 'lunatik', 'lwgjl', 'machine learning', 'make', 'mapping', 'mariadb', 'matlab', 'medical imaging', 'ml', 'mlir', 'mobile', 'mongodb', 'mysql', 'neo4j', 'networking', 'nlp', 'node.js', 'nodejs', 'nt', 'numba', 'numpy', 'ocaml', 'open source databases', 'opencl', 'opencv', 'opengl', 'openwrt', 'pallene', 'pcap', 'perl', 'php', 'posix', 'postgres', 'postgresql', 'programming-language', 'prometheus', 'pygame', 'python', 'python 3', 'qemu', 'qml', 'qt', 'r', 'r-project', 'rails', 'raspberry pi', 'rdf', 'react', 'react native', 'reactnative', 'redis', 'rest', 'risc-v', 'robotics', 'ros', 'rpc', 'rpm', 'ruby', 'ruby on rails', 'rust', 'sanitizers', 'scala', 'scheme', 'screwdriver', 'scripting', 'sdl', 'sdr', 'secure multi-party computation', 'servant', 'service mesh', 'shell', 'shell script', 'smb', 'solr', 'sound open firmware', 'space applications', 'spark', 'spinnaker', 'spring', 'sql', 'sqlite', 'svg', 'swift', 'swig', 'symfony', 'systemverilog', 'tcl', 'tcl/tk', 'tekton', 'templates', 'tensorflow', 'terminal-kit', 'terraform', 'twig', 'typescript', 'ui automation', 'unicode', 'unix', 'vaapi', 'vala', 'velocity', 'verilog', 'vhdl', 'virtualization', 'vue', 'vue.js', 'vulkan', 'wayland', 'web development', 'webkit', 'webpack', 'webrtc', 'win32', 'win32 api', 'wordpress', 'x11', 'x86', 'xen', 'xml', 'xmpp', 'xpath']

tag2019 = ['a-frame', 'ai', 'android', 'angular', 'angularjs', 'ansible', 'apache spark', 'app engine', 'arduino', 'arm', 'asr', 'assembler', 'assembly', 'asynchronous i/o', 'audio', 'automaton', 'automotive', 'awk', 'aws', 'bash', 'bazel', 'biojs', 'blender', 'boinc', 'bootstrap', 'bsd', 'bsd unix', 'bytecode', 'c', 'c#', 'c++', 'c++ libraries c++11 c++14 c++17 c++20', 'c++11', 'c++14', 'c++17', 'c/c++', 'c99', 'cabal', 'cakephp', 'chapel', 'clang', 'clojure', 'cloud', 'cmake', 'cms', 'codeworld', 'compiler', 'compilers', 'component-based development', 'containers', 'cpp', 'css', 'css3', 'cuda', 'cups', 'cython', 'c�u', 'd3', 'data analysis', 'database', 'deep learning', 'directx', 'distributed systems', 'django', 'dlang', 'docker', 'documentation', 'drones', 'drupal 8', 'elasicsearch', 'elasticsearch', 'electron', 'email', 'embedded', 'ffmpeg', 'flask', 'fonts', 'fortran', 'fpga', 'gazebo', 'gdal', 'gdscript', 'ghc', 'git', 'github', 'gnss', 'gnu autotools', 'gnu make', 'go', 'golang', 'google app engine', 'gradle', 'grafana', 'graphite', 'grpc', 'gstreamer', 'gtk', 'gtk+', 'gtkmm', 'gwt', 'hardware acceleration', 'haskell', 'hg', 'high performance computing', 'htc vive', 'html', 'html/css', 'html/css/js', 'html5', 'html5 canvas', 'html5/css3', 'iaccessible2', 'ide', 'influxdb', 'ionic', 'ios', 'ipp', 'irc', 'isabelle proof assistant', 'jakarta', 'java', 'javafx', 'javascript', 'jenkins', 'jinja2', 'jquery', 'json', 'jsonnet', 'julia', 'jupyter', 'jvm', 'kconfig',
           'kernel', 'kubernetes', 'kvm', 'latex', 'linux', 'linux kernel', 'lisp', 'llvm', 'lua', 'lwjgl', 'machine learning', 'make', 'maps api', 'mariadb', 'medical imaging', 'meteor.js', 'midi', 'mongodb', 'mpi', 'mysql', 'neo4j', 'networking', 'nlp', 'node.js', 'nodejs', 'nss', 'nt', 'numba', 'open source databases', 'open-sound-control', 'openapi', 'opencl', 'opencv', 'opengl', 'openj9', 'openmp', 'openwrt', 'operating systems', 'operator', 'os', 'osx', 'parallelization', 'patroni', 'perl', 'perl5', 'perl6', 'pharo', 'php', 'posix', 'postgres', 'postgresql', 'programming languages', 'prometheus', 'protocol buffers', 'python', 'python 3', 'qt', 'qt5', 'r', 'r-project', 'rails', 'raspberry pi', 'rdbms', 'react', 'react native', 'reactjs', 'redis', 'regular expressions', 'rest', 'risc-v', 'robotics', 'ros', 'rpc', 'ruby', 'ruby on rails', 'rust', 'scala', 'scripting', 'sdl', 'sdr', 'search', 'selenium', 'servant', 'server', 'shell', 'shell script', 'singularity', 'skala', 'smalltalk', 'smb', 'some/ip', 'sphinx', 'spir-v', 'spring', 'sql', 'sqlite', 'squeak', 'svg', 'swift', 'swig', 'symfony', 'tcl', 'tensorflow', 'terraform', 'tokio_rs', 'typescript', 'ui automation', 'unicode', 'unix', 'vega', 'vega-lite', 'velocity', 'verilog', 'vhdl', 'video', 'virtualization', 'voctomix', 'vulkan', 'wayland', 'web', 'web apps', 'web development', 'webasssembly', 'webcomponents', 'webgl', 'win32', 'win32 api', 'windows', 'wordpress', 'x11', 'x86', 'xen', 'xilinx', 'xml', 'xmpp', 'yocto']

tag2018 = ['advanced data structures', 'ai', 'android', 'android/ios', 'angular', 'angularjs', 'ansible', 'antlr', 'apache kafka', 'appengine', 'arduino', 'artificial intelligence', 'asm', 'assembly', 'audio', 'awk', 'bash', 'big data', 'blender', 'boinc', 'boost', 'bpm', 'browser extension', 'bsd make', 'bsd unix', 'c', 'c#', 'c++', 'c++11', 'c++14', 'c++17', 'c/c++', 'cad', 'cakephp', 'cassandra', 'ceph', 'chisel', 'clojure', 'cloud', 'cmake', 'cms', 'codecs', 'communication protocol', 'compression', 'computer vision', 'content management system', 'cpp', 'crossplatform', 'css', 'css/html', 'css3', 'cuda', 'cups', 'cython', 'c�u', 'd', 'd3', 'd3.js', 'dask', 'data analysis', 'database', 'databases', 'datproject', 'ddos', 'deep learning', 'dhcp', 'directx', 'distributed systems', 'django', 'docker', 'dpdk', 'drones', 'eclipse', 'elasticsearch', 'electron', 'elk', 'embedded', 'emberjs', 'erlang', 'espresso', 'ffmpeg', 'firmware', 'flask', 'fonts', 'fortran', 'fpga', 'framework', 'frontend', 'fsts', 'gazebo', 'gcc', 'git', 'github', 'gnss', 'gnu autotools', 'gnu make', 'gnupg', 'go', 'gobject', 'golang', 'graphql', 'groovy', 'grpc', 'gtk', 'gtk+', 'hadoop', 'hardware acceleration', 'haskell', 'hg', 'html', 'html/javascript', 'html5', 'html5/css3', 'hydra', 'hypervisor', 'ice - zeroc', 'ionic', 'ios', 'iot', 'ipp', 'isabelle proof assistant', 'isl', 'java', 'java script', 'javacc', 'javascript', 'javascript/html5/css3', 'jquery', 'jruby', 'json', 'json/json-ld', 'julia', 'jupyter',
           'jvm', 'kubernetes', 'kvm', 'lamp', 'linux', 'linux kernel', 'lisp', 'llvm', 'lua', 'lxc', 'machine learning', 'macos', 'make', 'mariadb', 'matlab', 'meteor.js', 'microservices', 'middleware', 'midi', 'mongodb', 'music', 'mysql', 'net', 'nltk', 'node', 'node.js', 'numba', 'object-oriented', 'ocaml', 'opencl', 'opencv', 'opengl', 'openmp', 'openscenegraph', 'opentracing', 'openvpn', 'openwrt', 'ordbms', 'parallelization', 'perl', 'php', 'php/javascript/ajax', 'php/javascript/html', 'physical computing', 'polly', 'posix', 'postgis', 'postgresql', 'ppcg', 'prometheus', 'pthon', 'pyth', 'python', 'python 3', 'qemu', 'qml', 'qt', 'r', 'r-project', 'rails', 'rdbms', 'rdf', 'react', 'react native', 'react.js', 'reactjs', 'real-time', 'redis', 'redux', 'remote access', 'rest', 'robotics', 'ros', 'rspec', 'ruby', 'ruby on rail', 'ruby on rails', 'rust', 'scala', 'scikit-learn', 'scilab', 'scripting', 'sdl', 'shell script', 'simd', 'singularity', 'smt', 'sockets', 'spark', 'sparql', 'sphinx', 'spring', 'sql', 'standards', 'svg', 'swift', 'swig', 'symfony', 'syntaxnet', 'synthesis', 'tcl', 'tcl/tk', 'tcp', 'tensorflow', 'tla+', 'twisted', 'typescript', 'unicode', 'unix', 'unreal engine', 'va-api', 'velocity', 'verilog', 'vhdl', 'video', 'vim', 'vue.js', 'vulkan', 'wayland', 'web', 'web development', 'web/html/css', 'webassembly', 'webcomponents', 'webgl', 'webkit', 'webrtc', 'webs', 'wiki', 'win32', 'windows', 'x11', 'xarray', 'xen', 'xia', 'xml', 'xmpp', 'xpath', 'xtext', 'yocto']

tag2021 = ['#js', '#jvm', '#llvm', '#scala', '#scala_lang', 'android', 'angular', 'antlr', 'apache airflow', 'api', 'arduino', 'arm', 'arrow', 'artificial intelligence', 'assembler', 'assembly', 'audio', 'aws', 'backend', 'bash', 'bibtex', 'big data science', 'boost', 'bsd unix', 'bytecode', 'c', 'c language', 'c++', 'c++11', 'c++14', 'c++17', 'c++20', 'canvas', 'ceph', 'chapel', 'ci', 'cifs', 'clang', 'cmake', 'compiler', 'computer vision', 'concurrency', 'container orchestration', 'coq', 'css', 'css3', 'cuda', 'cups', 'cython', 'c�u', 'dart', 'data analysis', 'data structures', 'decentralisation', 'deeplearning', 'devops', 'distributed systems', 'django', 'docker', 'drones', 'dsp', 'ebpf', 'elasticsearch', 'electron', 'elixir', 'elk', 'elm', 'embedded', 'embedded systems', 'ffmpeg', 'fhir', 'flutter', 'fortran', 'fossology', 'fpga', 'functional programming', 'fuzzing', 'gazebo', 'gdscript', 'ghc', 'gis', 'git', 'github-actions', 'glib', 'gnss', 'gnu autotools', 'gnu make', 'go', 'golang', 'gradle', 'graphql', 'gstreamer', 'gtk', 'gtkmm', 'guix', 'gwt', 'hadoop', 'haskell', 'hg', 'high performance computing', 'hl7 fhir', 'html', 'html5', 'hyperledger aries', 'hypervisor', 'ignition', 'instrumentation', 'internationalization', 'ios', 'ipp', 'irc', 'java', 'javafx', 'javascr', 'javascript', 'jenkins', 'json', 'julia', 'julialang', 'jupyter', 'jvm', 'kafka', 'kernel',
           'kotlin', 'kubernetes', 'kvm', 'latex', 'libxcam', 'linux', 'linux kernel', 'llvm', 'lua', 'lwjgl', 'machine learning', 'machinelearning', 'make', 'many more', 'mariadb', 'materialui', 'mbed', 'mediawiki', 'medical imaging', 'micropython', 'mlir', 'mongodb', 'mpi', 'mysql', 'namespaces', 'neo4j', 'networking', 'nlp', 'nltk', 'node', 'node.js', 'nodejs', 'nt', 'numba', 'numpy', 'ocaml', 'ocean technology', 'ogc standards', 'openapi', 'opencl', 'opencv', 'opengl', 'openmp', 'openwrt', 'openxr', 'ortelius', 'pandas', 'perl', 'pharo', 'php', 'posix', 'postgres', 'postgresql', 'programming-language', 'python', 'python 3', 'python deep learning frameworks', 'python gtk', 'pytorch', 'qml', 'qt', 'qt5', 'r', 'r-project', 'rails', 'raspberry pi', 'rdf', 'react', 'react native', 'redis', 'rest api', 'restful api', 'risc-v', 'roassal', 'robotics', 'ros', 'routing', 'ruby', 'ruby on rails', 'rust', 'scala', 'screwdriver.cd', 'scripting', 'sdl', 'sdr', 'shell', 'shell script', 'smalltalk', 'smb', 'spark', 'sparql', 'spec', 'spinnaker', 'spir-v', 'spring', 'sql', 'sqlalchemy', 'sqlite', 'statistics', 'swift', 'tekton', 'tensorflow', 'typescript', 'uefi', 'ui/ux', 'v4l2', 'vaapi', 'vala', 'velocity', 'verilog', 'vhdl', 'video codecs', 'virtualization', 'visualization', 'vue', 'vue.js', 'vulkan', 'wayland', 'web development', 'web services', 'webgpu', 'win32', 'x86', 'xen', 'xml', 'zmq']


def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return False
    else:
        return True


yeartag = ['#js', '#jvm', '#llvm', '#scala', '#scala_lang', '.net', 'a-frame', 'advanced data structures', 'ai', 'android', 'android/ios', 'angular', 'angularjs', 'ansible', 'antlr', 'apache airflow', 'apache kafka', 'apache spark', 'api', 'apis', 'app engine', 'appengine', 'arduino', 'arm', 'arrow', 'artificial intelligence', 'asm', 'asr', 'assembler', 'assembly', 'asynchronous i/o', 'audio', 'automaton', 'automotive', 'awk', 'aws', 'backend', 'bash', 'bazel', 'beam', 'bibtex', 'big data', 'big data science', 'biojs', 'blender', 'boinc', 'boost', 'bootstrap', 'bpm', 'browser extension', 'bsd', 'bsd make', 'bsd unix', 'buildbot', 'bytecode', 'c', 'c language', 'c#', 'c++', 'c++ libraries c++11 c++14 c++17 c++20', 'c++11', 'c++14', 'c++17', 'c++20', 'c/c++', 'c99', 'cabal', 'cad', 'cakephp', 'canvas', 'cassandra', 'ceph', 'chapel', 'chatbots', 'che', 'chisel', 'ci', 'ci/cd', 'cifs', 'clang', 'clojure', 'cloud', 'cmake', 'cms', 'codecs', 'codeworld', 'communication protocol', 'compiler', 'compilers', 'component-based development', 'compression', 'computer vision', 'concurrency', 'container orchestration', 'containers', 'content management system', 'coq', 'cpp', 'crossplatform', 'css', 'css/html', 'css3', 'cuda', 'cups', 'cython', 'céu', 'd', 'd3', 'd3.js', 'dart', 'dask', 'data analysis', 'data science', 'data structures', 'database', 'databases', 'datproject', 'ddos', 'decentralisation', 'deep learning', 'deeplearning', 'devops', 'dhcp', 'differential privacy', 'directx', 'distributed systems', 'django', 'dlang', 'docker', 'documentation', 'dpdk', 'drones', 'drupal 8', 'dsp', 'ebpf', 'eclipse', 'eclipsejavaide', 'elasicsearch', 'elasticsearch', 'electron', 'elixir', 'elk', 'elm', 'email', 'embedded', 'embedded systems', 'emberjs', 'erlang', 'espresso', 'federated learning', 'ffmpeg', 'fhir', 'firmware', 'flask', 'flutter', 'fonts', 'fortran', 'fossology', 'fpga', 'framework', 'frontend', 'fsts', 'functional programming', 'fuzzing', 'game development', 'gazebo', 'gcc', 'gdal', 'gdscript', 'ghc', 'gis', 'git', 'github', 'github-actions', 'glib', 'gnss', 'gnu autotools', 'gnu make', 'gnupg', 'go', 'gobject', 'golang', 'google app engine', 'google web toolkit', 'gradle', 'grafana', 'graphite', 'graphql', 'groovy', 'grpc', 'gstreamer', 'gtk', 'gtk+', 'gtkmm', 'guix', 'gwt', 'hadoop', 'hardware acceleration', 'haskell', 'hg', 'high performance computing', 'hl7 fhir', 'homomorphic encryption', 'honeypot', 'hpc', 'hpx', 'htc vive', 'html', 'html/css', 'html/css/js', 'html/javascript', 'html5', 'html5 canvas', 'html5/css3', 'hydra', 'hyperledger aries', 'hypervisor', 'iaccessible2', 'ice - zeroc', 'ide', 'ignition', 'influxdb', 'instrumentation', 'internationalization', 'ionic', 'ios', 'iot', 'ipp', 'irc', 'isabelle proof assistant', 'isl', 'jakarta', 'jakartaee', 'java', 'java script', 'javacc', 'javafx', 'javajava', 'javascr', 'javascript', 'javascript/html5/css3', 'jenkins', 'jinja2', 'jni', 'jquery', 'jruby', 'json', 'json/json-ld', 'jsonnet', 'julia', 'julialang', 'junit', 'jupyter', 'jupyter notebook', 'jvm', 'kafka', 'kconfig',
           'kernel', 'kibana', 'kotlin', 'kubernetes', 'kustomize', 'kvm', 'lamp', 'latex', 'lfe', 'libusb', 'libuv', 'libxcam', 'linkerd', 'linux', 'linux distribution', 'linux kernel', 'lisp', 'llvm', 'lua', 'lunatik', 'lwgjl', 'lwjgl', 'lxc', 'machine learning', 'machinelearning', 'macos', 'make', 'many more', 'mapping', 'maps api', 'mariadb', 'materialui', 'matlab', 'mbed', 'mediawiki', 'medical imaging', 'meteor.js', 'micropython', 'microservices', 'middleware', 'midi', 'ml', 'mlir', 'mobile', 'mongodb', 'mpi', 'music', 'mysql', 'namespaces', 'neo4j', 'net', 'networking', 'nlp', 'nltk', 'node', 'node.js', 'nodejs', 'nss', 'nt', 'numba', 'numpy', 'object-oriented', 'ocaml', 'ocean technology', 'ogc standards', 'open source databases', 'open-sound-control', 'openapi', 'opencl', 'opencv', 'opengl', 'openj9', 'openmp', 'openscenegraph', 'opentracing', 'openvpn', 'openwrt', 'openxr', 'operating systems', 'operator', 'ordbms', 'ortelius', 'os', 'osx', 'pallene', 'pandas', 'parallelization', 'patroni', 'pcap', 'perl', 'perl5', 'perl6', 'pharo', 'php', 'php/javascript/ajax', 'php/javascript/html', 'physical computing', 'polly', 'posix', 'postgis', 'postgres', 'postgresql', 'ppcg', 'programming languages', 'programming-language', 'prometheus', 'protocol buffers', 'pthon', 'pygame', 'pyth', 'python', 'python 3', 'python deep learning frameworks', 'python gtk', 'pytorch', 'qemu', 'qml', 'qt', 'qt5', 'r', 'r-project', 'rails', 'raspberry pi', 'rdbms', 'rdf', 'react', 'react native', 'react.js', 'reactjs', 'reactnative', 'real-time', 'redis', 'redux', 'regular expressions', 'remote access', 'rest', 'rest api', 'restful api', 'risc-v', 'roassal', 'robotics', 'ros', 'routing', 'rpc', 'rpm', 'rspec', 'ruby', 'ruby on rail', 'ruby on rails', 'rust', 'sanitizers', 'scala', 'scheme', 'scikit-learn', 'scilab', 'screwdriver', 'screwdriver.cd', 'scripting', 'sdl', 'sdr', 'search', 'secure multi-party computation', 'selenium', 'servant', 'server', 'service mesh', 'shell', 'shell script', 'simd', 'singularity', 'skala', 'smalltalk', 'smb', 'smt', 'sockets', 'solr', 'some/ip', 'sound open firmware', 'space applications', 'spark', 'sparql', 'spec', 'sphinx', 'spinnaker', 'spir-v', 'spring', 'sql', 'sqlalchemy', 'sqlite', 'squeak', 'standards', 'statistics', 'svg', 'swift', 'swig', 'symfony', 'syntaxnet', 'synthesis', 'systemverilog', 'tcl', 'tcl/tk', 'tcp', 'tekton', 'templates', 'tensorflow', 'terminal-kit', 'terraform', 'tla+', 'tokio_rs', 'twig', 'twisted', 'typescript', 'uefi', 'ui automation', 'ui/ux', 'unicode', 'unix', 'unreal engine', 'v4l2', 'va-api', 'vaapi', 'vala', 'vega', 'vega-lite', 'velocity', 'verilog', 'vhdl', 'video', 'video codecs', 'vim', 'virtualization', 'visualization', 'voctomix', 'vue', 'vue.js', 'vulkan', 'wayland', 'web', 'web apps', 'web development', 'web services', 'web/html/css', 'webassembly', 'webasssembly', 'webcomponents', 'webgl', 'webgpu', 'webkit', 'webpack', 'webrtc', 'webs', 'wiki', 'win32', 'win32 api', 'windows', 'wordpress', 'x11', 'x86', 'xarray', 'xen', 'xia', 'xilinx', 'xml', 'xmpp', 'xpath', 'xtext', 'yocto', 'zmq']


@gsocTags.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        year = request.form['year']

        tags = request.form.getlist('tags')
        if(year != ""):
            result = collection.find({"Year":year})
            org = []

            #if('all' not in tags):
            if tags: #If tags not empty, use the list. Else, take all as default
                for tag in tags:
                    for res in result:
                        if(tag in res['Tags']):
                            org.append(res)
                return render_template('index.html', data=org, tags=yeartag, year=year, count=len(org))
            else:
                return render_template('index.html', data=result, tags=yeartag, year=year, count=result.count())
        return render_template('index.html', data=[], tags=yeartag, year=year, count=0)
    else:
        result = collection.find({"Year": "2021"})
        year = "2021"
        org = []
        for res in result:
            org.append(res)
            # count += 1
        return render_template('index.html', data=org, tags=yeartag, year=year, count=len(org))


@gsocTags.route('/2021')
def gsoc2021fun():
    result = collection.find({"Year": "2021"})
    org = []
    for res in result:
        org.append(res)
    return render_template('index.html', data=org, tags=tag2021)


@gsocTags.route('/2020')
def gsoc2020fun():
    result = collection.find({"Year": "2020"})
    org = []
    for res in result:
        org.append(res)
    return render_template('index.html', data=org, tags=tag2020)


@gsocTags.route('/2019')
def gsoc2019fun():
    result = collection.find({"Year": "2019"})
    org = []
    for res in result:
        org.append(res)
    return render_template('index.html', data=org, tags=tag2019)


@gsocTags.route('/2018')
def gsoc2018fun():
    result = collection.find({"Year": "2019"})
    org = []
    for res in result:
        org.append(res)
    return render_template('index.html', data=org, tags=tag2018)


if __name__ == '__main__':
    gsocTags.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    gsocTags.run()
