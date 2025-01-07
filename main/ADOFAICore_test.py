import ADOFAICore_cython_compile,time


if __name__ == '__main__':
  res = 0;
  for i in range(20):
    s = time.time();
    convert = ADOFAICore_cython_compile.adofai_level_data.new("18616.adofai")
    convert.decode()
    e = time.time();
    res += e-s
    print(e-s)
  print()
  print(res/20)