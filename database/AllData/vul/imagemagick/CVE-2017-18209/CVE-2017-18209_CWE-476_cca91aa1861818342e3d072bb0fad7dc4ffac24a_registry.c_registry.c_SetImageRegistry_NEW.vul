MagickExport MagickBooleanType SetImageRegistry(const RegistryType type,
  const char *key,const void *value,ExceptionInfo *exception)
{
  MagickBooleanType
    status;

  RegistryInfo
    *registry_info;

  void
    *clone_value;

  if (IsEventLogging() != MagickFalse)
    (void) LogMagickEvent(TraceEvent,GetMagickModule(),"%s",key);
  if (value == (const void *) NULL)
    return(MagickFalse);
  clone_value=(void *) NULL;
  switch (type)
  {
    case StringRegistryType:
    default:
    {
      const char
        *string;

      string=(const char *) value;
      clone_value=(void *) ConstantString(string);
      break;
    }
    case ImageRegistryType:
    {
      const Image
        *image;

      image=(const Image *) value;
      if (image->signature != MagickCoreSignature)
        {
          (void) ThrowMagickException(exception,GetMagickModule(),RegistryError,
            "UnableToSetRegistry","%s",key);
          return(MagickFalse);
        }
      clone_value=(void *) CloneImageList(image,exception);
      break;
    }
    case ImageInfoRegistryType:
    {
      const ImageInfo
        *image_info;

      image_info=(const ImageInfo *) value;
      if (image_info->signature != MagickCoreSignature)
        {
          (void) ThrowMagickException(exception,GetMagickModule(),RegistryError,
            "UnableToSetRegistry","%s",key);
          return(MagickFalse);
        }
      clone_value=(void *) CloneImageInfo(image_info);
      break;
    }
  }
  if (clone_value == (void *) NULL)
    return(MagickFalse);
  registry_info=(RegistryInfo *) AcquireCriticalMemory(sizeof(*registry_info));
  (void) ResetMagickMemory(registry_info,0,sizeof(*registry_info));
  registry_info->type=type;
  registry_info->value=clone_value;
  registry_info->signature=MagickCoreSignature;
  if (registry == (SplayTreeInfo *) NULL)
    {
      if (registry_semaphore == (SemaphoreInfo *) NULL)
        ActivateSemaphoreInfo(&registry_semaphore);
      LockSemaphoreInfo(registry_semaphore);
      if (registry == (SplayTreeInfo *) NULL)
        registry=NewSplayTree(CompareSplayTreeString,RelinquishMagickMemory,
          DestroyRegistryNode);
      UnlockSemaphoreInfo(registry_semaphore);
    }
  status=AddValueToSplayTree(registry,ConstantString(key),registry_info);
  return(status);
}
