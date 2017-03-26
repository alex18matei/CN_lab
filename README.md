# Rezolvarea sistemelor liniare

- [x] Interfață
  - Scroll-ul merge foarte încet
- [x] Documentație
- [x] Metoda gradienților bi-conjugați stabilizată
- [x] Testat pe toate matricile
  - Pe matricea 4 nu dă bine, dar pe celelalte trei, plus pe una găsită pe net,
    dă corect. Soluția matricei 4 are niște "?!?!" în PDF, deci probabil că
    acolo e ok.


# Matrici rare

- [x] Reprezentare
- [x] Verificare număr maxim de elemente pe linie
- [x] Comparare matrici
- [x] Adunare matrici
- [x] Înmulțire cu vector
- [x] Înmulțire cu matrici
- [x] Interfață
- [x] Refactorizare
- [x] Optimizare
  - Cel mai mult timp e petrecut în buclele din `Matrix#add_item()`. Încă nu
    prea știu cum să le optimizez. Pe laptop-ul meu, `matmul()` ia 23.3 sec.
  - Dacă transform tema 3 în modul de Cython, pe laptop-ul meu `nogui()` scade
    de la ~44 sec la ~19 sec.
  - Se poate optimiza și mai mult, dacă folosesc trei vectori în loc de un
    singur vector de tuple, dar ar fi mult de modificat.


# Inversa unei matrice

- [ ] interfata grafica
- [ ] bonus 15p


# Aproximarea valorilor şi vectorilor proprii, SVD

- [x] Aproximarea valorilor și vectorilor proprii
- [ ] SVD
  - Mai am de făcut ultima parte din enunț.
- [x] Interfață
