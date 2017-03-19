# Rezolvarea sistemelor liniare

- [ ] Reparat bug
- [ ] Metoda gradienților bi-conjugați stabilizată
  - Documentație
- [ ] Testat pe toate matricile

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
