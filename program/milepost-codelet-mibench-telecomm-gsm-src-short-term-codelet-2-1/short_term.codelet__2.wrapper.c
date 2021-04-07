/* 
 Codelet from MILEPOST project: http://cTuning.org/project-milepost
 Updated by Grigori Fursin to work with Collective Mind Framework

 3 "./short_term.codelet__2.wrapper.c" 3 4
*/

#include <stdio.h>

int __astex_write_message(const char * format, ...);
int __astex_write_output(const char * format, ...);
void __astex_exit_on_error(const char * msg, int code, const char * additional_msg);
void * __astex_fopen(const char * name, const char * mode);
void * __astex_memalloc(long bytes);
void __astex_close_file(void * file);
void __astex_read_from_file(void * dest, long bytes, void * file);
int __astex_getenv_int(const char * var);
void * __astex_start_measure();
double __astex_stop_measure(void * _before);
typedef short  word;
typedef long  longword;
typedef unsigned long  ulongword;
void  astex_codelet__2(word *rp, int k_n, word *s, word *u, longword ltmp);
int main(int argc, const char **argv)
{
  word  *rp;
  int  k_n = 13;
  word  *s;
  word  *u;
  longword  ltmp = 5380656l;
  void * codelet_data_file_descriptor = (void *) 0;

#ifdef OPENME
  openme_init(NULL,NULL,NULL,0);
  openme_callback("PROGRAM_START", NULL);
#endif

  if (argc < 2)
    __astex_exit_on_error("Please specify data file in command-line.", 1, argv[0]);
  codelet_data_file_descriptor = __astex_fopen(argv[1], "rb");
  
  char * rp__region_buffer = (char *) __astex_memalloc(16);
  __astex_write_message("Reading rp value from %s\n", argv[1]);
  __astex_read_from_file(rp__region_buffer, 16, codelet_data_file_descriptor);
  rp = (word *) (rp__region_buffer + 0l);
  char * s__region_buffer = (char *) __astex_memalloc(320);
  __astex_write_message("Reading s value from %s\n", argv[1]);
  __astex_read_from_file(s__region_buffer, 320, codelet_data_file_descriptor);
  s = (word *) (s__region_buffer + 0l);
  char * u__region_buffer = (char *) __astex_memalloc(656);
  __astex_write_message("Reading u value from %s\n", argv[1]);
  __astex_read_from_file(u__region_buffer, 656, codelet_data_file_descriptor);
  u = (word *) (u__region_buffer + 580l);
  void * _astex_timeval_before = __astex_start_measure();
  int _astex_wrap_loop = __astex_getenv_int("CT_REPEAT_MAIN");
  if (! _astex_wrap_loop)
    _astex_wrap_loop = 1;

#ifdef OPENME
  openme_callback("KERNEL_START", NULL);
#endif

  while (_astex_wrap_loop > 0)
  {
    --_astex_wrap_loop;
  astex_codelet__2(rp, k_n, s, u, ltmp);

  }

#ifdef OPENME
  openme_callback("KERNEL_END", NULL);
#endif

  __astex_write_output("Total time: %lf\n", __astex_stop_measure(_astex_timeval_before));


#ifdef OPENME
  openme_callback("PROGRAM_END", NULL);
#endif

  return 0;
}

