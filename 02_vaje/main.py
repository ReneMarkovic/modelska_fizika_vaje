from RLS.raketa import raketa

FNM_X0 = raketa(m_gorivo = 1_000)

dt = 0.01
FNM_X0.simuliraj(dt)
FNM_X0.izvozi_rezultate()