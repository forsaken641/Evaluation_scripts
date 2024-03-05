static int MagickDLLCall PostscriptDelegateMessage(void *handle,
  const char *message,int length)
{
  char
    **messages;

  ssize_t
    offset;

  offset=0;
  messages=(char **) handle;
  if (*messages == (char *) NULL)
    *messages=(char *) AcquireQuantumMemory(length+1,sizeof(char *));
  else
    {
      offset=strlen(*messages);
      *messages=(char *) ResizeQuantumMemory(*messages,offset+length+1,
        sizeof(char *));
    }
  if (*messages == (char *) NULL)
    return(0);
  (void) memcpy(*messages+offset,message,length);
  (*messages)[length+offset] ='\0';
  return(length);
}
