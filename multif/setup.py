from distutils.core import setup, Extension

setup(ext_modules=[ \
      Extension("_meshutils_module",
      sources=["./meshutils/meshutils_py.c", \
 				"./meshutils/meshutils.c", \
 				 "./meshutils/GMFio.c", \
 				 "./meshutils/SU2io.c", \
 				 "./meshutils/clean.c", \
 				 "./meshutils/extraction.c", \
 				 "./meshutils/libmesh6.c", \
 				 "./meshutils/modules.c", \
 				 "./meshutils/utils.c", \
 				 "./meshutils/parser.c", \
 				 "./meshutils/option.c", \
 				 "./meshutils/mesh.c", \
 				 "./meshutils/nozzle.c", \
 				 "./meshutils/bspline3.c", \
 				 "./meshutils/piecewise.c", \
 				 "./meshutils/meshutils_py.i", \
			     "./meshutils/projection.c", \
 				 "./meshutils/GMSHio.c"],
       extra_compile_args=["-std=c99","-Wno-unused-variable","-Wno-unused-result"]),
       
       Extension('_nozzle_module',
       sources = ['./meshutils/nozzle.cpp'],
       extra_compile_args=["-Wno-maybe-uninitialized","-std=c++11","-Wno-sign-compare","-Wno-unused-but-set-variable","-DHAVE_NO_OCC_CONFIG_H"],
       libraries=['Gmsh','TKOffset', 'TKTopAlgo', 'TKGeomAlgo', 'TKBRep', 'TKGeomBase', 'TKG3d', 'TKG2d',
                  'TKMath', 'TKernel', 'TKBool', 'TKFeat', 'TKShHealing']),
       
       Extension("_mshint_module",
       sources=["./mshint/boule.c"      , \
			    "./mshint/bucket.c"     , \
			    "./mshint/chrono.c"     , \
			    "./mshint/hash.c"       , \
			    "./mshint/inout.c"      , \
			    "./mshint/intelt.c"     , \
			    "./mshint/libmesh5.c"   , \
			    "./mshint/locelt.c"     , \
			    "./mshint/mshin1.c"     , \
			    "./mshint/mshint.c"     , \
			    "./mshint/mshint_py.c"  , \
			    "./mshint/mshint_py.i"  , \
			    "./mshint/GMFio.c" , \
			    "./mshint/SU2io.c" , \
			    "./mshint/mesh.c" ,\
			    "./mshint/scalem.c"] , \
	   extra_compile_args=["-O3","-c","-Wuninitialized","-Wunused",
	   "-Winline","-Wshadow","-fexpensive-optimizations","-funroll-loops"]),   
       
       Extension("./SU2/amginria/_amgio",
       sources=[ "./SU2/amginria/amgio/amgio_py.c", \
       			 "./SU2/amginria/amgio/mesh.c", \
       			 "./SU2/amginria/amgio/GMFio.c", \
       			 "./SU2/amginria/amgio/SU2io.c", \
       			 "./SU2/amginria/amgio/option.c", \
       			 "./SU2/amginria/amgio/libmesh6.c", \
                 "./SU2/amginria/amgio/amgio_py.i", \
       			 "./SU2/amginria/amgio/convert.c"],
        extra_compile_args=["-std=c99","-Wno-unused-variable","-Wno-unused-result"]), 
       
	   
	  Extension("LOWF/_quasi1dnozzle",
      sources=["./LOWF/quasi1dnozzle_py.c", \
               "./LOWF/lofinozzle.c", \
               "./LOWF/odeint.c", \
               "./meshutils/piecewise.c", \
               "./LOWF/quasi1dnozzle_py.i"],
      extra_compile_args=["-std=c99","-Wno-unused-variable","-Wno-unused-result"])
    
       ]);
       
       
       
