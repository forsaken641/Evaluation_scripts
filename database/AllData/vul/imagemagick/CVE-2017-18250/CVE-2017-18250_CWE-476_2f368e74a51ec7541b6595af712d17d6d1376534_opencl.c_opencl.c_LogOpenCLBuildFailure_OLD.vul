static void LogOpenCLBuildFailure(MagickCLDevice device,const char *kernel,
  ExceptionInfo *exception)
{
  char
    filename[MagickPathExtent],
    *log;

  size_t
    log_size;

  (void) FormatLocaleString(filename,MagickPathExtent,"%s%s%s",
    GetOpenCLCacheDirectory(),DirectorySeparator,"magick_badcl.cl");

  (void) remove_utf8(filename);
  (void) BlobToFile(filename,kernel,strlen(kernel),exception);

  openCL_library->clGetProgramBuildInfo(device->program,device->deviceID,
    CL_PROGRAM_BUILD_LOG,0,NULL,&log_size);
  log=(char*)AcquireMagickMemory(log_size);
  openCL_library->clGetProgramBuildInfo(device->program,device->deviceID,
    CL_PROGRAM_BUILD_LOG,log_size,log,&log_size);

  (void) FormatLocaleString(filename,MagickPathExtent,"%s%s%s",
    GetOpenCLCacheDirectory(),DirectorySeparator,"magick_badcl.log");

  (void) remove_utf8(filename);
  (void) BlobToFile(filename,log,log_size,exception);
  log=(char*)RelinquishMagickMemory(log);
}
