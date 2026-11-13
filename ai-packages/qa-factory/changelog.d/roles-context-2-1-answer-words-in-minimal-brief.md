- Brief (`brief_pack.py`): at the most compressed level the line of a free-text answer to a question now carries the
  person's words, cut at the same length as the other decision lines, with a pointer to `<decisions>` when cut; the
  same words under several questions are still given once, and the kept-open and not-needed lines are unchanged.
