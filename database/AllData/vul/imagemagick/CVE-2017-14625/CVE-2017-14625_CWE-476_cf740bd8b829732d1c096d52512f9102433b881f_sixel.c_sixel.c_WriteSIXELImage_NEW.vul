static MagickBooleanType WriteSIXELImage(const ImageInfo *image_info,
  Image *image,ExceptionInfo *exception)
{
  MagickBooleanType
    status;

  register const Quantum
    *q;

  register ssize_t
    i,
    x;

  ssize_t
    opacity,
    y;

  sixel_output_t
    *output;

  unsigned char
    sixel_palette[256*3],
    *sixel_pixels;

  /*
    Open output image file.
  */
  assert(image_info != (const ImageInfo *) NULL);
  assert(image_info->signature == MagickCoreSignature);
  assert(image != (Image *) NULL);
  assert(image->signature == MagickCoreSignature);
  if (image->debug != MagickFalse)
    (void) LogMagickEvent(TraceEvent,GetMagickModule(),"%s",image->filename);
  status=OpenBlob(image_info,image,WriteBinaryBlobMode,exception);
  if (status == MagickFalse)
    return(status);
  if (IssRGBCompatibleColorspace(image->colorspace) == MagickFalse)
    (void) TransformImageColorspace(image,sRGBColorspace,exception);
  opacity=(-1);
  if (image->alpha_trait == UndefinedPixelTrait)
    {
      if ((image->storage_class == DirectClass) || (image->colors > 256))
        (void) SetImageType(image,PaletteType,exception);
    }
  else
    {
      MagickRealType
        alpha,
        beta;

      /*
        Identify transparent colormap index.
      */
      if ((image->storage_class == DirectClass) || (image->colors > 256))
        (void) SetImageType(image,PaletteBilevelAlphaType,exception);
      for (i=0; i < (ssize_t) image->colors; i++)
        if (image->colormap[i].alpha != OpaqueAlpha)
          {
            if (opacity < 0)
              {
                opacity=i;
                continue;
              }
            alpha=image->colormap[i].alpha;
            beta=image->colormap[opacity].alpha;
            if (alpha < beta)
              opacity=i;
          }
      if (opacity == -1)
        {
          (void) SetImageType(image,PaletteBilevelAlphaType,exception);
          for (i=0; i < (ssize_t) image->colors; i++)
            if (image->colormap[i].alpha != OpaqueAlpha)
              {
                if (opacity < 0)
                  {
                    opacity=i;
                    continue;
                  }
                alpha=image->colormap[i].alpha;
                beta=image->colormap[opacity].alpha;
                if (alpha < beta)
                  opacity=i;
              }
        }
      if (opacity >= 0)
        {
          image->colormap[opacity].red=image->transparent_color.red;
          image->colormap[opacity].green=image->transparent_color.green;
          image->colormap[opacity].blue=image->transparent_color.blue;
        }
    }
  /*
    SIXEL header.
  */
  for (i=0; i < (ssize_t) image->colors; i++)
  {
    sixel_palette[3*i+0]=ScaleQuantumToChar(image->colormap[i].red);
    sixel_palette[3*i+1]=ScaleQuantumToChar(image->colormap[i].green);
    sixel_palette[3*i+2]=ScaleQuantumToChar(image->colormap[i].blue);
  }

  /*
    Define SIXEL pixels.
  */
  output = sixel_output_create(image);
  if (output == (sixel_output_t *) NULL)
    ThrowWriterException(ResourceLimitError,"MemoryAllocationFailed");
  sixel_pixels=(unsigned char *) AcquireQuantumMemory(image->columns,
    image->rows*sizeof(*sixel_pixels));
  if (sixel_pixels == (unsigned char *) NULL)
    {
      output = (sixel_output_t *) RelinquishMagickMemory(output);
      ThrowWriterException(ResourceLimitError,"MemoryAllocationFailed");
    }
  for (y=0; y < (ssize_t) image->rows; y++)
  {
    q=GetVirtualPixels(image,0,y,image->columns,1,exception);
    if (q == (Quantum *) NULL)
      break;
    for (x=0; x < (ssize_t) image->columns; x++)
    {
      sixel_pixels[y*image->columns+x]= ((ssize_t) GetPixelIndex(image,q));
      q+=GetPixelChannels(image);
    }
  }
  status = sixel_encode_impl(sixel_pixels,image->columns,image->rows,
    sixel_palette,image->colors,-1,output);
  sixel_pixels=(unsigned char *) RelinquishMagickMemory(sixel_pixels);
  output=(sixel_output_t *) RelinquishMagickMemory(output);
  (void) CloseBlob(image);
  return(status);
}
