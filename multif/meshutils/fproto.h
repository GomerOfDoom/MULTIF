/*
Victorien Menier Feb 2016
*/

////--- cad.c
//int        Geo2Egads ();
//static int spline1d(ego    context, int    imax, double *x, double *y, double *z, ego    *ecurv);
//int 			 WriteEgads (char *Nam, Cad *cad);
//int				 WriteEgadsSurf (char *Nam, Cad *cad);
//
////--- cad_gmsh.c
//Cad* AllocGeo (int *CadSiz);
//Cad* FreeGeo (Cad *cad);
//int  GetGeoSize (char *GeoNam, int *CadSiz);
//int  ReadGeo (char *GeoNam, Cad *cad);

//--- projection.c
int NozzleWallProjection (Options *mshopt, Mesh *Msh, CadNozzle * CadNoz, int refUp, int refDown, char *OutNam);
int ProjectToDV(double *Crd, CadNozzle *Noz, double *BasParam, int Patch);
int NozzleWallProjection_DV (Options *mshopt, Mesh *Msh, CadNozzle * CadNoz, CadNozzle * CadNoz_bas, int refUp, int refDown, char *OutNam, int verbose);


//--- extraction.c
int SolutionExtraction(Options *mshopt, Mesh *Msh);
double * ExtractAlongLine (Options *mshopt, Mesh *Msh, double *box, int *NbrRes, int *Siz);
double * ExtractSolutionAtRef (Options *mshopt, Mesh *Msh, int *Ref, int NbrRef,  int *NbrRes, int *Siz);
int Extract_Vertices_Ref (Options *mshopt, Mesh *Msh, int Ref, double *Crd_Out, int *Vid_Out, int *Nbv);

//--- GMFio.c
int AddGMFMeshSize (char *MshNam, int *SizMsh);
int LoadGMFMesh (char *MshNam, Mesh *Msh);
int LoadGMFSolution(char *SolNam, Mesh *Msh);
int WriteGMFMesh(char *nam, Mesh *Msh, int OptBin);
int WriteGMFSolution(char *SolNam, double *Sol, int SolSiz, int NbrVer, int Dim, int NbrFld, int* FldTab);
int WriteGMFSolutionItf(char *SolNam, Mesh *Msh);
int WriteSegMesh(char *nam, Mesh *Msh);

//---- mesh.c
Mesh* AllocMesh (int * SizMsh);
int   cmp_int2(const void *a, const void *b);
int   FreeMesh (Mesh *Msh);
int   GetMeshSize (char *MshNam, int *SizMsh);
Mesh *SetupMeshAndSolution (char *MshNam, char *SolNam);
int   RemoveUnconnectedVertices (Mesh *Msh);
void  AddEdge(Mesh *Msh, int idx, int *is, int ref);
void  AddHexahedron(Mesh *Msh, int idx, int *is, int ref);
void  AddQuadrilateral(Mesh *Msh, int idx, int *is, int ref);
void  AddTetrahedron(Mesh *Msh, int idx, int *is, int ref);
void  AddPyramid(Mesh *Msh, int idx, int *is, int ref);
void  AddPrism(Mesh *Msh, int idx, int *is, int ref);
void  AddTriangle(Mesh *Msh, int idxTri, int *is, int ref);
void  AddVertex(Mesh *Msh, int idxVer, double *Crd);
int   imin(int n, int *idx);
void  PrintMeshInfo (Mesh *Msh);
void  switchHexIdx(int *idx, int *swi);
void  switchQuaIdx(int *idx, int *swi);
void  switchTetIdx(int *idx, int *swi);
void  switchTriIdx(int *idx, int *swi);

//--- modules.c
int    ConvertGMFtoSU2Sol (Options *mshopt);
int    ConvertSU2SolToGMF (Options *mshopt);
int    Extraction (Options *mshopt);
int    OutputMach (Options *mshopt);
int    ConvertSU2ToGMSH (Options *mshopt);
int    ProjectNozzleWall (Options *mshopt);
int    ConvertGMFtoSegMesh (Options *mshopt);
Mesh * ExtractSurfacePatches(Mesh *Msh, int *Ref, int NbrRef) ;

//--- option.c
Options* AllocOptions(void);
int      CheckOptions (Options *mshopt);
int      GetBasNam (char *InpNam, char *BasNam);
void     PrintOptions (Options *mshopt);

//--- parser.c
int  GetInputFileType (char *FilNam);
int  ParseCommandLine (Options *mshopt,int argc, char *argv[]);
void Usage(void);

//--- SU2io.c
int  AddSU2MeshSize (char *FilNam, int *SizMsh) ;
int  GetSU2KeywordValue (FILE *FilHdl, char *Kwd);
int  GetSU2KeywordValueStr (FILE *FilHdl, char *Kwd, char *StrVal);
int  LoadSU2Elements(FILE *FilHdl, Mesh *Msh);
int  LoadSU2Mesh (char *FilNam, Mesh *Msh);
int  LoadSU2Solution(char *SolNam, Mesh *Msh);
int  LoadSU2Vertices (FILE *FilHdl, Mesh *Msh);
void WriteSU2Mesh(char *nam, Mesh *Msh);
int  WriteSU2Solution (char *SolNam, Mesh *Msh, double *Sol, int NbrVer, int SolSiz, char SolTag[100][256]);

//--- GMSHio.c
void WriteGMSHMesh(char *nam, Mesh *Msh);

//--- utils.c
int  Str2Lower(char *buff);
void StrRemoveChars (char* str, char c);

//--- nozzle.c
int          FreeCadBspline (CadBspline *Bsp);
int          LoadCadBspline (char *BasNam, CadBspline *Bsp, int verbose);
int 		 SetCadBspline (CadBspline *Bsp, double *Knots, int NbrKnots, double *Coefs, int NbrCoefs);
CadBspline * AllocCadBspline (int NbrCoefs, int NbrKnots);
int          GetCadBsplineSize ( char *BasNam , int *NbrCoefs, int *NbrKnots );
CadNozzle *  AllocCadNozzle (int * SizCad);
int          FreeCadNozzle (CadNozzle *Noz) ;
double       fzcut (double x,  double *BasParam);
double       fycut (double x,  double *BasParam);
double 		 fz_bas (double x,  double *BasParam);
double 		 fr1_bas (double x,  double *BasParam);
double 		 fr2_bas (double x,  double *BasParam);
int        WriteCadBspline(char *BasNam, CadBspline *Bsp, int verbose);
int        Evaluate_Nozzle ( CadNozzle *Noz, double *x, double *r1, double *r2, double *zcenter );

//--- Bspline

/* Forward search through array for first element greater than a given xFind */
int find(double xFind, double *xVec, int size);

/* 3rd degree B-spline mapping from parametric u to coordinates x, y, and 
   derivatives */
void uMap3(double *knots, double *coefs, double u, double *x, double *y,
	   double *dxdu, double *dydu, int k, int c);

/* Given x and B-spline parameters, calculate y and dydx for 2-D 3rd degree 
   B-spline */
void bSplineGeo3(double *knots, double *coefs, double *x, double *y,
		 double *dydx, int nx, int k, int c);

//--- Piecewise Linear
//void piecewiseLinear(double *xnodes, double *ynodes, double *x, double *y,
//		     double *dydx, int nx, int nn);
void interp1(double *xn, double *yn, int nn, double *x, double *y, int nx, int js);
void interp1grad(double *xn, double *yn, int nn, double *x, double *dydx, int nx, int js);
		     
