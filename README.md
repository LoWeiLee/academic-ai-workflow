# academic-ai-workflow

**一人研究團隊之 AI 學術協作工作流。** 七道工序、四份控制檔模板、一個資料夾治理基座，把大型語言模型變成可稽核的研究助理。

**AI Academic Collaboration Workflow for a Solo Research Team.** Seven pipelined skills, four control-file templates, and a governed folder base that turn a large language model into an auditable research assistant.

![Workflow architecture / 工作流架構](docs/workflow-architecture.jpg)

最一開始，這套工作流並不是有意識的設計，而是偶然底下的產物。近期我覺得 AI 模型的能力越來越接近我的要求，從前必須不斷解釋自己的想法(雖然過程中也幫我自己聚焦)，但目前只要提出粗略概念他就能與我交換意見並幫我聚焦，於是我開始更頻繁的與 AI 討論研究想法。今年2月份左右我與 AI 來回討論一篇撰寫中的期刊架構，AI 第一次主動在對話告一段落後，產出一份清楚且品質不錯摘要，並提示我未來可以這份文件為基礎開始撰寫工作，這非常像過往我每次寫paper時，都會為自己撰寫的架構型筆記。於是我便問 AI，要如何確保未來每一份研究、每一篇期刊都能產出這份筆記，接著便有了整個工作流的開端，research-desing-diagnosis.md。

很快的，我意識到必須把這個單點skill擴展成一整套學術研究工作流，包括研究設計、文獻搜尋、逐篇分析、跨篇綜整、章節撰寫、審稿診斷到質性主題分析(量化分析模板會在未來加入)。看到這裡你應該可以發現，這其實就是研究者們都很熟悉的研究方法流程圖，只是我在每個階段都加入 AI 可以參與輔助的設計。這套工作流的核心主張是：AI 輔助研究的品質與誠信問題，這不是「提示詞寫得夠不夠好」的技巧問題，而是制度缺席的治理問題。

在這套工作流底下，你可以：
1. 和 AI 討論研究想法，他每次都會按照既定的架構與你對話，並協助你將結果整理出一份品質穩定的筆記(research-desing-diagnosis)
2. 透過學術資料庫 API 讓AI去幫你找文獻，依照你設計的關鍵字幫你做初步篩選，並交付給你作最後裁決(literature-search)
3. 對每篇文獻進行深度分析，產出理論基本知識與在當前的應用方向(literature-analysis)
4. 你可以把多篇分析整合為帶明確文獻歸屬的理論知識圖譜，一切基於前階段的真實文獻(literature-synthesis)
5. 搭配 Obsidian 等雙向連結工具建成跨專案文獻庫；你可以基於既定全文結構與論述方向，將上述綜整成果落筆為文章初稿，並進一步進行修訂(chapter-drafting)
6. 要求 AI 扮演討人厭的挑剔審稿人，對稿件進行審查(review-diagnosis)
7. 針對訪談逐字稿走 reflexive TA 或 coding reliability 路線，進行質性主題分析(thematic-analysis)。

你或許會問，為什麼沒有量化分析的 skill 模板？這是來自作者本身的偏誤，量化是我的老本行，我寫得太習慣了，單獨做一支 skill 不符合成本效益。另外就是，我已經做了另一個統計前端工具多多快跑(https://loweilee.github.io/duoduorun/) ，來做為輔助教學工具。

還有一件事，什麼該進執行層自動化、什麼必須留在使用者手上，這個判斷只有每天親手做研究的你做得出來。有興趣的人可以上網搜尋「員工 0 人的稅務師畠山謙人」，這段話來自於畠山，而我深有共鳴。他在稅務領域，將自己的工作流明確切割，並與 AI 充分協作，這套研究工作流長成現在的樣子，是社會科學領域的我，在自己熟悉的研究中，一刀一刀迭代出來的，不是套用任何現成工具的預設。因此我認為，所有想試試這套協作工作流的研究者也應如此：把這七支 skill 當成起點與參照，依自己的工作狀況裁剪增刪，而不是照單全收。

最後，如果你想試試套 AI 協作工作流，我也邀請你回饋使用經驗，讓整套架構能夠不斷進化。

Read the full README in ／ 完整說明請選擇語言：　**[English](README_EN.md)**　｜　**[繁體中文](README_CHT.md)**
