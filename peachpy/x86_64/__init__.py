# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


import sys

import peachpy.x86_64.abi
import peachpy.x86_64.uarch
import peachpy.x86_64.isa


from peachpy.x86_64.registers import GeneralPurposeRegister, \
    GeneralPurposeRegister8, GeneralPurposeRegister16, GeneralPurposeRegister32, GeneralPurposeRegister64, \
    MMXRegister, XMMRegister, YMMRegister, ZMMRegister, KRegister, \
    rax, rbx, rcx, rdx, rsi, rdi, rbp, r8, r9, r10, r11, r12, r13, r14, r15, \
    eax, ebx, ecx, edx, esi, edi, ebp, r8d, r9d, r10d, r11d, r12d, r13d, r14d, r15d, \
    ax, bx, cx, dx, si, di, bp, r8w, r9w, r10w, r11w, r12w, r13w, r14w, r15w, \
    al, ah, bl, bh, cl, ch, dl, dh, sil, dil, bpl, r8b, r9b, r10b, r11b, r12b, r13b, r14b, r15b, \
    mm0, mm1, mm2, mm3, mm4, mm5, mm6, mm7, \
    xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8, xmm9, xmm10, xmm11, xmm12, xmm13, xmm14, xmm15, \
    xmm16, xmm17, xmm18, xmm19, xmm20, xmm21, xmm22, xmm23, xmm24, xmm25, xmm26, xmm27, xmm28, xmm29, xmm30, xmm31, \
    ymm0, ymm1, ymm2, ymm3, ymm4, ymm5, ymm6, ymm7, ymm8, ymm9, ymm10, ymm11, ymm12, ymm13, ymm14, ymm15, \
    ymm16, ymm17, ymm18, ymm19, ymm20, ymm21, ymm22, ymm23, ymm24, ymm25, ymm26, ymm27, ymm28, ymm29, ymm30, ymm31, \
    zmm0, zmm1, zmm2, zmm3, zmm4, zmm5, zmm6, zmm7, zmm8, zmm9, zmm10, zmm11, zmm12, zmm13, zmm14, zmm15, \
    zmm16, zmm17, zmm18, zmm19, zmm20, zmm21, zmm22, zmm23, zmm24, zmm25, zmm26, zmm27, zmm28, zmm29, zmm30, zmm31, \
    k0, k1, k2, k3, k4, k5, k6, k7
from peachpy.x86_64.function import Function, LocalVariable
from peachpy.x86_64.operand import byte, word, dword, qword, oword, hword, yword, zword, \
    rn_sae, rz_sae, ru_sae, rd_sae, sae

from peachpy.x86_64.pseudo import Label, Loop, \
    LABEL, ALIGN, RETURN, LOAD, STORE, SWAP, REDUCE
from peachpy.x86_64.nacl import NACLJMP

from peachpy.x86_64.generic import \
    ADD, SUB, ADC, SBB, ADCX, ADOX, \
    AND, OR, XOR, ANDN, \
    NOT, NEG, INC, DEC, \
    TEST, CMP, \
    MOV, MOVZX, MOVSX, MOVSXD, MOVBE, MOVNTI, \
    BT, BTS, BTR, BTC, POPCNT, BSWAP, \
    BSF, BSR, LZCNT, TZCNT, \
    SHR, SAR, SHL, SAL, SHRX, SARX, SHLX, \
    SHRD, SHLD, \
    ROR, ROL, RORX, \
    RCR, RCL, \
    IMUL, MUL, MULX, \
    IDIV, DIV, \
    LEA, PUSH, POP, \
    POPCNT, LZCNT, TZCNT, \
    BEXTR, PDEP, PEXT, \
    BZHI, \
    BLCFILL, BLCI, BLCIC, BLCMSK, BLCS, \
    BLSFILL, BLSI, BLSIC, BLSMSK, BLSR, \
    T1MSKC, TZMSK, \
    CRC32, \
    CBW, CDQ, CQO, \
    CWD, CWDE, CDQE, \
    CMOVA, CMOVNA, CMOVAE, CMOVNAE, \
    CMOVB, CMOVNB, CMOVBE, CMOVNBE, \
    CMOVC, CMOVNC, CMOVE, CMOVNE, \
    CMOVG, CMOVNG, CMOVGE, CMOVNGE, \
    CMOVL, CMOVNL, CMOVLE, CMOVNLE, \
    CMOVO, CMOVNO, CMOVP, CMOVNP, \
    CMOVS, CMOVNS, CMOVZ, CMOVNZ, \
    CMOVPE, CMOVPO, \
    SETA, SETNA, SETAE, SETNAE, \
    SETB, SETNB, SETBE, SETNBE, \
    SETC, SETNC, SETE, SETNE, \
    SETG, SETNG, SETGE, SETNGE, \
    SETL, SETNL, SETLE, SETNLE, \
    SETO, SETNO, SETP, SETNP, \
    SETS, SETNS, SETZ, SETNZ, \
    SETPE, SETPO, \
    JA, JNA, JAE, JNAE, \
    JB, JNB, JBE, JNBE, \
    JC, JNC, JE, JNE, \
    JG, JNG, JGE, JNGE, \
    JL, JNL, JLE, JNLE, \
    JO, JNO, JP, JNP, \
    JS, JNS, JZ, JNZ, \
    JPE, JPO, JMP, \
    JRCXZ, JECXZ, \
    RET, CALL, \
    PAUSE, NOP, \
    INT, UD2, \
    CPUID, RDTSC, RDTSCP, XGETBV, \
    STC, CLC, CMC, \
    STD, CLD, \
    XADD, XCHG, \
    CMPXCHG, CMPXCHG8B, CMPXCHG16B, \
    SFENCE, MFENCE, LFENCE, \
    PREFETCHNTA, PREFETCHT0, PREFETCHT1, PREFETCHT2

from peachpy.x86_64.mmxsse import \
    MOVSS, EXTRACTPS, INSERTPS, \
    ADDSS, SUBSS, MULSS, DIVSS, SQRTSS, \
    ROUNDSS, MINSS, MAXSS, RCPSS, RSQRTSS, \
    CMPSS, COMISS, UCOMISS, \
    MOVSD, ADDSD, SUBSD, MULSD, DIVSD, SQRTSD, \
    ROUNDSD, MINSD, MAXSD, \
    CMPSD, COMISD, UCOMISD, \
    MOVAPS, MOVUPS, MOVLPS, MOVNTPS, \
    MOVHPS, MOVSLDUP, MOVSHDUP, \
    MOVAPD, MOVUPD, MOVLPD, MOVNTPD, \
    MOVHPD, MOVDDUP, \
    ADDPS, HADDPS, SUBPS, HSUBPS, ADDSUBPS, MULPS, DIVPS, SQRTPS, \
    ADDPD, HADDPD, SUBPD, HSUBPD, ADDSUBPD, MULPD, DIVPD, SQRTPD, \
    ROUNDPS, MINPS, MAXPS, RCPPS, RSQRTPS, DPPS, \
    CMPPS, MOVMSKPS, \
    ROUNDPD, MINPD, MAXPD, DPPD, \
    CMPPD, MOVMSKPD, \
    ANDPS, ANDNPS, ORPS, XORPS, BLENDPS, BLENDVPS, \
    ANDPD, ANDNPD, ORPD, XORPD, BLENDPD, BLENDVPD, \
    UNPCKLPS, UNPCKHPS, MOVLHPS, MOVHLPS, SHUFPS, \
    UNPCKLPD, UNPCKHPD, SHUFPD, \
    MOVD, MOVQ, MOVDQ2Q, MOVQ2DQ, MOVDQA, MOVDQU, LDDQU, \
    MASKMOVQ, MASKMOVDQU, \
    MOVNTQ, MOVNTDQ, MOVNTDQA, \
    PMOVSXBW, PMOVSXBD, PMOVSXBQ, PMOVSXWD, PMOVSXWQ, PMOVSXDQ, \
    PMOVZXBW, PMOVZXBD, PMOVZXBQ, PMOVZXWD, PMOVZXWQ, PMOVZXDQ, \
    PEXTRB, PEXTRW, PEXTRD, PEXTRQ, \
    PINSRB, PINSRW, PINSRD, PINSRQ, \
    PMOVMSKB, PTEST, \
    PADDB, PADDW, PADDD, PADDQ, PADDSB, PADDSW, PADDUSB, PADDUSW, \
    PHADDW, PHADDD, PHADDSW, \
    PSUBB, PSUBW, PSUBD, PSUBQ, PSUBSB, PSUBSW, PSUBUSB, PSUBUSW, \
    PHSUBW, PHSUBD, PHSUBSW, \
    PMAXSB, PMAXSW, PMAXSD, PMAXUB, PMAXUW, PMAXUD, \
    PMINSB, PMINSW, PMINSD, PMINUB, PMINUW, PMINUD, \
    PSLLW, PSLLD, PSLLQ, PSRLW, PSRLD, PSRLQ, PSRAW, PSRAD, \
    PMULLW, PMULHW, PMULHUW, PMULLD, PMULDQ, PMULUDQ, \
    PMULHRSW, PMADDWD, PMADDUBSW, \
    PAVGB, PAVGW, \
    PSADBW, MPSADBW, PHMINPOSUW, \
    PCMPEQB, PCMPEQW, PCMPEQD, PCMPEQQ, \
    PCMPGTB, PCMPGTW, PCMPGTD, PCMPGTQ, \
    PABSB, PABSW, PABSD, PSIGNB, PSIGNW, PSIGND, \
    PAND, PANDN, POR, PXOR, PBLENDW, PBLENDVB, \
    PUNPCKLBW, PUNPCKLWD, PUNPCKLDQ, PUNPCKLQDQ, \
    PUNPCKHBW, PUNPCKHWD, PUNPCKHDQ, PUNPCKHQDQ, \
    PACKSSWB, PACKSSDW, PACKUSWB, PACKUSDW, \
    PSHUFB, PSHUFW, PSHUFLW, PSHUFHW, PSHUFD, \
    PSLLDQ, PSRLDQ, PALIGNR, \
    PCMPESTRI, PCMPESTRM, PCMPISTRI, PCMPISTRM, \
    CVTSS2SI, CVTTSS2SI, CVTSI2SS, \
    CVTSD2SI, CVTTSD2SI, CVTSI2SD, \
    CVTPS2DQ, CVTTPS2DQ, CVTDQ2PS, \
    CVTPD2DQ, CVTTPD2DQ, CVTDQ2PD, \
    CVTPS2PI, CVTTPS2PI, CVTPI2PS, \
    CVTPD2PI, CVTTPD2PI, CVTPI2PD, \
    CVTSD2SS, CVTSS2SD, \
    CVTPD2PS, CVTPS2PD, \
    LDMXCSR, STMXCSR, \
    EMMS

from peachpy.x86_64.avx import \
    VMOVSS, VEXTRACTPS, VINSERTPS, \
    VADDSS, VSUBSS, VMULSS, VDIVSS, VSQRTSS, \
    VROUNDSS, VRNDSCALESS, VRANGESS, \
    VMINSS, VMAXSS, VREDUCESS, \
    VGETMANTSS, VGETEXPSS, VSCALEFSS, VFIXUPIMMSS, VFPCLASSSS, \
    VRCPSS, VRSQRTSS, VRCP14SS, VRSQRT14SS, VRCP28SS, VRSQRT28SS, \
    VCMPSS, VCOMISS, VUCOMISS, \
    VMOVSD, VADDSD, VSUBSD, VMULSD, VDIVSD, VSQRTSD, \
    VROUNDSD, VRNDSCALESD, VRANGESD, \
    VMINSD, VMAXSD, VREDUCESD, \
    VGETMANTSD, VGETEXPSD, VSCALEFSD, VFIXUPIMMSD, VFPCLASSSD, \
    VRCP14SD, VRSQRT14SD, VRCP28SD, VRSQRT28SD, \
    VCMPSD, VCOMISD, VUCOMISD, \
    VMOVAPS, VMOVUPS, VMOVLPS, VMOVHPS, \
    VMASKMOVPS, VMOVMSKPS, VMOVNTPS, \
    VBROADCASTSS, VMOVSLDUP, VMOVSHDUP, \
    VEXPANDPS, VCOMPRESSPS, \
    VGATHERDPS, VGATHERQPS, \
    VGATHERPF0DPS, VGATHERPF0QPS, \
    VGATHERPF1DPS, VGATHERPF1QPS, \
    VSCATTERDPS, VSCATTERQPS, \
    VSCATTERPF0DPS, VSCATTERPF0QPS, \
    VSCATTERPF1DPS, VSCATTERPF1QPS, \
    VMOVAPD, VMOVUPD, VMOVLPD, VMOVHPD, \
    VMASKMOVPD, VMOVMSKPD, VMOVNTPD, \
    VBROADCASTSD, VMOVDDUP, \
    VEXPANDPD, VCOMPRESSPD, \
    VGATHERDPD, VGATHERQPD, \
    VGATHERPF0DPD, VGATHERPF0QPD, \
    VGATHERPF1DPD, VGATHERPF1QPD, \
    VSCATTERDPD, VSCATTERQPD, \
    VSCATTERPF0DPD, VSCATTERPF0QPD, \
    VSCATTERPF1DPD, VSCATTERPF1QPD, \
    VADDPS, VHADDPS, VSUBPS, VHSUBPS, VADDSUBPS, VMULPS, VDIVPS, VSQRTPS, \
    VADDPD, VHADDPD, VSUBPD, VHSUBPD, VADDSUBPD, VMULPD, VDIVPD, VSQRTPD, \
    VROUNDPS, VRNDSCALEPS, VRANGEPS, \
    VMINPS, VMAXPS, VREDUCEPS, VDPPS, \
    VGETMANTPS, VGETEXPPS, VSCALEFPS, VFIXUPIMMPS, VFPCLASSPS, \
    VRCPPS, VRSQRTPS, VRCP14PS, VRSQRT14PS, VRCP28PS, VRSQRT28PS, VEXP2PS, \
    VCMPPS, VTESTPS, \
    VROUNDPD, VRNDSCALEPD, VRANGEPD, \
    VMINPD, VMAXPD, VREDUCEPD, VDPPD, \
    VGETMANTPD, VGETEXPPD, VSCALEFPD, VFIXUPIMMPD, VFPCLASSPD, \
    VRCP14PD, VRSQRT14PD, VRCP28PD, VRSQRT28PD, VEXP2PD, \
    VCMPPD, VTESTPD, \
    VANDPS, VANDNPS, VORPS, VXORPS, VBLENDPS, VBLENDVPS, VBLENDMPS, \
    VANDPD, VANDNPD, VORPD, VXORPD, VBLENDPD, VBLENDVPD, VBLENDMPD, \
    VUNPCKLPS, VUNPCKHPS, VMOVLHPS, VMOVHLPS, VSHUFPS, \
    VUNPCKLPD, VUNPCKHPD, VSHUFPD, \
    VPERMPS, VPERMILPS, VPERMT2PS, VPERMI2PS, \
    VPERMPD, VPERMILPD, VPERMT2PD, VPERMI2PD, \
    VMOVD, VMOVQ, VMOVDQA, VMOVDQA32, VMOVDQA64, \
    VMOVDQU, VMOVDQU8, VMOVDQU16, VMOVDQU32, VMOVDQU64, VLDDQU, \
    VPBROADCASTB, VPBROADCASTW, VPBROADCASTD, VPBROADCASTQ, \
    VPEXPANDD, VPEXPANDQ, \
    VPCOMPRESSD, VPCOMPRESSQ, \
    VPMASKMOVD, VPMASKMOVQ, VMASKMOVDQU, VMOVNTDQ, VMOVNTDQA, \
    VPMOVSXBW, VPMOVSXBD, VPMOVSXBQ, VPMOVSXWD, VPMOVSXWQ, VPMOVSXDQ, \
    VPMOVZXBW, VPMOVZXBD, VPMOVZXBQ, VPMOVZXWD, VPMOVZXWQ, VPMOVZXDQ, \
    VPMOVWB, VPMOVDB, VPMOVDW, VPMOVQB, VPMOVQW, VPMOVQD, \
    VPMOVSWB, VPMOVSDB, VPMOVSDW, VPMOVSQB, VPMOVSQW, VPMOVSQD, \
    VPMOVUSWB, VPMOVUSDB, VPMOVUSDW, VPMOVUSQB, VPMOVUSQW, VPMOVUSQD, \
    VPEXTRB, VPEXTRW, VPEXTRD, VPEXTRQ, \
    VPINSRB, VPINSRW, VPINSRD, VPINSRQ, \
    VPGATHERDD, VPGATHERDQ, VPGATHERQD, VPGATHERQQ, \
    VPSCATTERDD, VPSCATTERDQ, VPSCATTERQD, VPSCATTERQQ, \
    VPCONFLICTD, VPCONFLICTQ, \
    VPLZCNTD, VPLZCNTQ, \
    VPTEST, VPMOVMSKB, \
    VPADDB, VPADDW, VPADDD, VPADDQ, VPADDSB, VPADDSW, VPADDUSB, VPADDUSW, \
    VPHADDW, VPHADDD, VPHADDSW, \
    VPSUBB, VPSUBW, VPSUBD, VPSUBQ, VPSUBSB, VPSUBSW, VPSUBUSB, VPSUBUSW, \
    VPHSUBW, VPHSUBD, VPHSUBSW, \
    VPMAXSB, VPMAXSW, VPMAXSD, VPMAXSQ, VPMAXUB, VPMAXUW, VPMAXUD, VPMAXUQ, \
    VPMINSB, VPMINSW, VPMINSD, VPMINSQ, VPMINUB, VPMINUW, VPMINUD, VPMINUQ, \
    VPSLLW, VPSLLD, VPSLLQ, VPSRLW, VPSRLD, VPSRLQ, VPSRAW, VPSRAD, VPSRAQ, \
    VPROLD, VPROLQ, VPRORD, VPRORQ, \
    VPSLLVW, VPSLLVD, VPSLLVQ, VPSRLVW, VPSRLVD, VPSRLVQ, VPSRAVW, VPSRAVD, VPSRAVQ, \
    VPROLVD, VPROLVQ, VPRORVD, VPRORVQ, \
    VPMULLW, VPMULHW, VPMULHUW, VPMULLD, VPMULLQ, VPMULDQ, VPMULUDQ, \
    VPMULHRSW, VPMADDWD, VPMADDUBSW, \
    VPMADD52LUQ, VPMADD52HUQ, \
    VPAVGB, VPAVGW, \
    VPSADBW, VMPSADBW, VDBPSADBW, VPHMINPOSUW, \
    VPCMPEQB, VPCMPEQW, VPCMPEQD, VPCMPEQQ, \
    VPCMPGTB, VPCMPGTW, VPCMPGTD, VPCMPGTQ, \
    VPCMPB, VPCMPW, VPCMPD, VPCMPQ, \
    VPCMPUB, VPCMPUW, VPCMPUD, VPCMPUQ, \
    VPABSB, VPABSW, VPABSD, VPABSQ, VPSIGNB, VPSIGNW, VPSIGND, \
    VPAND, VPANDD, VPANDQ, VPANDN, VPANDND, VPANDNQ, \
    VPOR, VPORD, VPORQ, VPXOR, VPXORD, VPXORQ, \
    VPTERNLOGD, VPTERNLOGQ, \
    VPBLENDW, VPBLENDVB, VPBLENDD, \
    VPBLENDMB, VPBLENDMW, VPBLENDMD, VPBLENDMQ, \
    VPUNPCKLBW, VPUNPCKLWD, VPUNPCKLDQ, VPUNPCKLQDQ, \
    VPUNPCKHBW, VPUNPCKHWD, VPUNPCKHDQ, VPUNPCKHQDQ, \
    VPACKSSWB, VPACKSSDW, VPACKUSWB, VPACKUSDW, \
    VPSHUFB, VPSHUFLW, VPSHUFHW, VPSHUFD, \
    VPERMB, VPERMW, VPERMD, VPERMQ, \
    VPERMT2B, VPERMT2W, VPERMT2D, VPERMT2Q, \
    VPERMI2B, VPERMI2W, VPERMI2D, VPERMI2Q, \
    VPSLLDQ, VPSRLDQ, VPALIGNR, VALIGND, VALIGNQ, VPMULTISHIFTQB, \
    VPCMPESTRI, VPCMPESTRM, VPCMPISTRI, VPCMPISTRM, \
    VCVTSS2SI, VCVTSS2USI, VCVTTSS2SI, VCVTTSS2USI, VCVTSI2SS, VCVTUSI2SS, \
    VCVTSD2SI, VCVTSD2USI, VCVTTSD2SI, VCVTTSD2USI, VCVTSI2SD, VCVTUSI2SD, \
    VCVTPS2DQ, VCVTPS2UDQ, VCVTTPS2DQ, VCVTTPS2UDQ, VCVTDQ2PS, VCVTUDQ2PS, \
    VCVTPS2QQ, VCVTPS2UQQ, VCVTTPS2QQ, VCVTTPS2UQQ, VCVTQQ2PS, VCVTUQQ2PS, \
    VCVTPD2DQ, VCVTPD2UDQ, VCVTTPD2DQ, VCVTTPD2UDQ, VCVTDQ2PD, VCVTUDQ2PD, \
    VCVTPD2QQ, VCVTPD2UQQ, VCVTTPD2QQ, VCVTTPD2UQQ, VCVTQQ2PD, VCVTUQQ2PD, \
    VCVTSD2SS, VCVTSS2SD, \
    VCVTPD2PS, VCVTPS2PD, \
    VCVTPS2PH, VCVTPH2PS, \
    VBROADCASTF128, VBROADCASTI128, \
    VBROADCASTF32X2, VBROADCASTI32X2, \
    VBROADCASTF32X4, VBROADCASTI32X4, \
    VBROADCASTF32X8, VBROADCASTI32X8, \
    VBROADCASTF64X2, VBROADCASTI64X2, \
    VBROADCASTF64X4, VBROADCASTI64X4, \
    VEXTRACTF128, VEXTRACTI128, \
    VEXTRACTF32X4, VEXTRACTI32X4, \
    VEXTRACTF32X8, VEXTRACTI32X8, \
    VEXTRACTF64X2, VEXTRACTI64X2, \
    VEXTRACTF64X4, VEXTRACTI64X4, \
    VINSERTF128, VINSERTI128, \
    VINSERTF32X4, VINSERTI32X4, \
    VINSERTF32X8, VINSERTI32X8, \
    VINSERTF64X2, VINSERTI64X2, \
    VINSERTF64X4, VINSERTI64X4, \
    VPERM2F128, VPERM2I128, \
    VSHUFF32X4, VSHUFI32X4, \
    VSHUFF64X2, VSHUFI64X2, \
    VPTESTMB, VPTESTMW, VPTESTMD, VPTESTMQ, \
    VPTESTNMB, VPTESTNMW, VPTESTNMD, VPTESTNMQ, \
    VLDMXCSR, VSTMXCSR, \
    VZEROUPPER, VZEROALL

from peachpy.x86_64.fma import \
    VFMADD132SS,  VFMADD213SS,  VFMADD231SS,  VFMADDSS, \
    VFMSUB132SS,  VFMSUB213SS,  VFMSUB231SS,  VFMSUBSS, \
    VFNMADD132SS, VFNMADD213SS, VFNMADD231SS, VFNMADDSS, \
    VFNMSUB132SS, VFNMSUB213SS, VFNMSUB231SS, VFNMSUBSS, \
    VFMADD132SD,  VFMADD213SD,  VFMADD231SD,  VFMADDSD, \
    VFMSUB132SD,  VFMSUB213SD,  VFMSUB231SD,  VFMSUBSD, \
    VFNMADD132SD, VFNMADD213SD, VFNMADD231SD, VFNMADDSD, \
    VFNMSUB132SD, VFNMSUB213SD, VFNMSUB231SD, VFNMSUBSD, \
    VFMADD132PS,  VFMADD213PS,  VFMADD231PS,  VFMADDPS, \
    VFMSUB132PS,  VFMSUB213PS,  VFMSUB231PS,  VFMSUBPS, \
    VFNMADD132PS, VFNMADD213PS, VFNMADD231PS, VFNMADDPS, \
    VFNMSUB132PS, VFNMSUB213PS, VFNMSUB231PS, VFNMSUBPS, \
    VFMADD132PD,  VFMADD213PD,  VFMADD231PD,  VFMADDPD, \
    VFMSUB132PD,  VFMSUB213PD,  VFMSUB231PD,  VFMSUBPD, \
    VFNMADD132PD, VFNMADD213PD, VFNMADD231PD, VFNMADDPD, \
    VFNMSUB132PD, VFNMSUB213PD, VFNMSUB231PD, VFNMSUBPD, \
    VFMADDSUB132PS, VFMADDSUB213PS, VFMADDSUB231PS, VFMADDSUBPS, \
    VFMSUBADD132PS, VFMSUBADD213PS, VFMSUBADD231PS, VFMSUBADDPS, \
    VFMADDSUB132PD, VFMADDSUB213PD, VFMADDSUB231PD, VFMADDSUBPD, \
    VFMSUBADD132PD, VFMSUBADD213PD, VFMSUBADD231PD, VFMSUBADDPD

from peachpy.x86_64.mask import \
    KADDB, KADDW, KADDD, KADDQ, \
    KANDB, KANDW, KANDD, KANDQ, \
    KANDNB, KANDNW, KANDND, KANDNQ, \
    KORB, KORW, KORD, KORQ, \
    KXNORB, KXNORW, KXNORD, KXNORQ, \
    KXORB, KXORW, KXORD, KXORQ, \
    KMOVB, KMOVW, KMOVD, KMOVQ, \
    KNOTB, KNOTW, KNOTD, KNOTQ, \
    KUNPCKBW, KUNPCKWD, KUNPCKDQ, \
    KTESTB, KTESTW, KTESTD, KTESTQ, \
    KORTESTB, KORTESTW, KORTESTD, KORTESTQ, \
    KSHIFTLB, KSHIFTLW, KSHIFTLD, KSHIFTLQ, \
    KSHIFTRB, KSHIFTRW, KSHIFTRD, KSHIFTRQ

from peachpy.x86_64.crypto import \
    AESDEC, AESDECLAST, AESENC, AESENCLAST, AESIMC, AESKEYGENASSIST, \
    VAESDEC, VAESDECLAST, VAESENC, VAESENCLAST, VAESIMC, VAESKEYGENASSIST, \
    SHA1MSG1, SHA1MSG2, SHA1NEXTE, SHA1RNDS4, SHA256MSG1, SHA256MSG2, SHA256RNDS2, \
    PCLMULQDQ, VPCLMULQDQ, \
    RDRAND, RDSEED

from peachpy.x86_64.amd import \
    PAVGUSB, PMULHRW, \
    PF2ID, PF2IW, PI2FW, PI2FD, \
    PFADD, PFSUB, PFSUBR, PFMUL, PFMAX, PFMIN, \
    PFACC, PFNACC, PFPNACC, PSWAPD, \
    PFCMPEQ, PFCMPGT, PFCMPGE, \
    PFRCP, PFRCPIT1, PFRCPIT2, PFRSQRT, PFRSQIT1, \
    FEMMS, \
    MOVNTSS, MOVNTSD, \
    INSERTQ, EXTRQ, \
    VPPERM, VPCMOV, \
    VPROTB, VPROTW, VPROTD, VPROTQ, \
    VPSHAB, VPSHAW, VPSHAD, VPSHAQ, \
    VPSHLB, VPSHLW, VPSHLD, VPSHLQ, \
    VPCOMB, VPCOMW, VPCOMD, VPCOMQ, \
    VPCOMUB, VPCOMUW, VPCOMUD, VPCOMUQ, \
    VPHADDBW, VPHADDBD, VPHADDBQ, VPHADDWD, VPHADDWQ, VPHADDDQ, \
    VPHADDUBW, VPHADDUBD, VPHADDUBQ, VPHADDUWD, VPHADDUWQ, VPHADDUDQ, \
    VPHSUBBW, VPHSUBWD, VPHSUBDQ, \
    VPMACSDQH, VPMACSDQL, VPMACSDD, VPMACSWD, VPMACSWW, VPMADCSWD, \
    VPMACSSDD, VPMACSSDQH, VPMACSSDQL, VPMACSSWD, VPMACSSWW, VPMADCSSWD, \
    VFRCZSS, VFRCZSD, VFRCZPS, VFRCZPD, \
    VPERMIL2PD, VPERMIL2PS

from peachpy.x86_64.types import \
    m64, m128, m128d, m128i, m256, m256d, m256i, m512, m512d, m512i, mmask8, mmask16
