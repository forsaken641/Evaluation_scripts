static HENHMETAFILE ReadEnhMetaFile(const char *path,ssize_t *width,
  ssize_t *height)
{
#pragma pack( push, 2 )
  typedef struct
  {
    DWORD dwKey;
    WORD hmf;
    SMALL_RECT bbox;
    WORD wInch;
    DWORD dwReserved;
    WORD wCheckSum;
  } APMHEADER, *PAPMHEADER;
#pragma pack( pop )

  DWORD
    dwSize;

  ENHMETAHEADER
    emfh;

  HANDLE
    hFile;

  HDC
    hDC;

  HENHMETAFILE
    hTemp;

  LPBYTE
    pBits;

  METAFILEPICT
    mp;

  HMETAFILE
    hOld;

  *width=512;
  *height=512;
  hTemp=GetEnhMetaFile(path);
#if defined(MAGICKCORE_HAVE__WFOPEN)
  if (hTemp == (HENHMETAFILE) NULL)
    {
      wchar_t
        *unicode_path;

      unicode_path=ConvertUTF8ToUTF16((const unsigned char *) path);
      if (unicode_path != (wchar_t *) NULL)
        {
          hTemp=GetEnhMetaFileW(unicode_path);
          unicode_path=(wchar_t *) RelinquishMagickMemory(unicode_path);
        }
    }
#endif
  if (hTemp != (HENHMETAFILE) NULL)
    {
      /*
        Enhanced metafile.
      */
      GetEnhMetaFileHeader(hTemp,sizeof(ENHMETAHEADER),&emfh);
      *width=emfh.rclFrame.right-emfh.rclFrame.left;
      *height=emfh.rclFrame.bottom-emfh.rclFrame.top;
      return(hTemp);
    }
  hOld=GetMetaFile(path);
  if (hOld != (HMETAFILE) NULL)
    {
      /*
        16bit windows metafile.
      */
      dwSize=GetMetaFileBitsEx(hOld,0,NULL);
      if (dwSize == 0)
        {
          DeleteMetaFile(hOld);
          return((HENHMETAFILE) NULL);
        }
      pBits=(LPBYTE) AcquireQuantumMemory(dwSize,sizeof(*pBits));
      if (pBits == (LPBYTE) NULL)
        {
          DeleteMetaFile(hOld);
          return((HENHMETAFILE) NULL);
        }
      if (GetMetaFileBitsEx(hOld,dwSize,pBits) == 0)
        {
          pBits=(BYTE *) DestroyString((char *) pBits);
          DeleteMetaFile(hOld);
          return((HENHMETAFILE) NULL);
        }
      /*
        Make an enhanced metafile from the windows metafile.
      */
      mp.mm=MM_ANISOTROPIC;
      mp.xExt=1000;
      mp.yExt=1000;
      mp.hMF=NULL;
      hDC=GetDC(NULL);
      hTemp=SetWinMetaFileBits(dwSize,pBits,hDC,&mp);
      ReleaseDC(NULL,hDC);
      DeleteMetaFile(hOld);
      pBits=(BYTE *) DestroyString((char *) pBits);
      GetEnhMetaFileHeader(hTemp,sizeof(ENHMETAHEADER),&emfh);
      *width=emfh.rclFrame.right-emfh.rclFrame.left;
      *height=emfh.rclFrame.bottom-emfh.rclFrame.top;
      return(hTemp);
    }
  /*
    Aldus Placeable metafile.
  */
  hFile=CreateFile(path,GENERIC_READ,0,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,
    NULL);
  if (hFile == INVALID_HANDLE_VALUE)
    return(NULL);
  dwSize=GetFileSize(hFile,NULL);
  pBits=(LPBYTE) AcquireQuantumMemory(dwSize,sizeof(*pBits));
  ReadFile(hFile,pBits,dwSize,&dwSize,NULL);
  CloseHandle(hFile);
  if (((PAPMHEADER) pBits)->dwKey != 0x9ac6cdd7l)
    {
      pBits=(BYTE *) DestroyString((char *) pBits);
      return((HENHMETAFILE) NULL);
    }
  /*
    Make an enhanced metafile from the placable metafile.
  */
  mp.mm=MM_ANISOTROPIC;
  mp.xExt=((PAPMHEADER) pBits)->bbox.Right-((PAPMHEADER) pBits)->bbox.Left;
  *width=mp.xExt;
  mp.xExt=(mp.xExt*2540l)/(DWORD) (((PAPMHEADER) pBits)->wInch);
  mp.yExt=((PAPMHEADER)pBits)->bbox.Bottom-((PAPMHEADER) pBits)->bbox.Top;
  *height=mp.yExt;
  mp.yExt=(mp.yExt*2540l)/(DWORD) (((PAPMHEADER) pBits)->wInch);
  mp.hMF=NULL;
  hDC=GetDC(NULL);
  hTemp=SetWinMetaFileBits(dwSize,&(pBits[sizeof(APMHEADER)]),hDC,&mp);
  ReleaseDC(NULL,hDC);
  pBits=(BYTE *) DestroyString((char *) pBits);
  return(hTemp);
}
