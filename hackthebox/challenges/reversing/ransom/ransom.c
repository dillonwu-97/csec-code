int encrypt(void* arg1, int arg2) {
      int64_t var_17 = 0x4345535245505553
      int16_t var_f = 0x5255
      char var_d = 0x45
      int32_t var_c = 0
      int64_t rax_16
      while (true)
          rax_16 = sx.q(var_c)
          if (arg2 u<= rax_16)
              break
          int64_t rcx = sx.q(var_c)
          int64_t rax_6
          int64_t rdx_1
          rdx_1:rax_6 = mulu.dp.q(rcx, 0x2e8ba2e8ba2e8ba3)
          uint64_t rdx_2 = rdx_1 u>> 1
          uint64_t rax_9 = rdx_2 * 5
          *(arg1 + sx.q(var_c)) = *(&var_17 + rcx - (rax_9 + rax_9 + rdx_2)) + *(arg1 + sx.q(var_c))
          var_c = var_c + 1
      return rax_16

}