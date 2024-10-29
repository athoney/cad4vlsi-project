~/cad4vlsi/lab03 $ sis
sis>

sis> read_pla demo.pla
sis> print
  {F} = A B' C' D + A' B C D + A' B C' D + A' B' C D + A' B' C' D
sis> simplify
sis> print
  {F} = A' D + B' C' D