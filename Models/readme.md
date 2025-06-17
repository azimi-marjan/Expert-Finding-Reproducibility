# 🧠 Expert Finding Models

This directory contains implementations of the four expert finding models evaluated in our paper:

---

## 📘 CB (Concatenated-Profile Based Model)

In this model, we concatenate all documents written by an author into a single profile.  
We then index and rank these profile documents using [Pyserini](https://github.com/castorini/pyserini).

---

## 📘 DB (Document-Based Model)

To run this model:

1. Use Pyserini to generate a language model based on the dataset and query set.
2. Use the resulting document-query scores as input to the `DB_model`, which ranks authors based on document-level evidence.

---

## 📘 DSEF (Document-Score + Network-Based Model)

This model extends the DB approach by incorporating network information:

1. Generate document-query language model scores using Pyserini (same as in DB).
2. Calculate degree centrality for each author based on the citation network.
3. Run `DSEF_model.py` to combine both evidence types (document scores + network centrality) for expert ranking.

---

## 📘 ExpFinder

We use the official implementation of **ExpFinder** provided by Kang et al. (2023).  
The code is available at the following link:  
🔗 [https://codeocean.com/capsule/5151827/tree/v1](https://codeocean.com/capsule/5151827/tree/v1)

---

## 📚 Citation

If you use the ExpFinder implementation or reference it in your work, please cite:

```bibtex
@article{kang2023expfinder,
  title={ExpFinder: A hybrid model for expert finding from text-based expertise data},
  author={Kang, Yong-Bin and Du, Hung and Forkan, Abdur Rahim Mohammad and Jayaraman, Prem Prakash and Aryani, Amir and     Sellis, Timos},
  journal={Expert Systems with Applications},
  volume={211},
  pages={118691},
  year={2023},
  publisher={Elsevier}
}
