### Interactive Visualization of Single-Cell RNA Sequencing Data in Traumatic Brain Injury Research

Chloe Zhang(017383066)

#### Problem Statement

The primary goal of this project is to facilitate the interactive exploration and analysis of single-cell RNA sequencing (scRNA-seq) data from traumatic brain injury (TBI) patients. Specifically, the visualization tool aims to:

- Provide an overview of cellular behavior under **both** different conditions and time points.
- Identify potential genes that play crucial roles in disease development and progression.
- Enable researchers to interactively filter and visualize the data to uncover patterns and insights.

#### Dataset and Data Abstraction

**Dataset:** The dataset comprises single-cell RNA sequencing data from TBI patients(private dataset). The data includes information on different cell types across three conditions (healthy, mild, severe) and three time points (day 1, day 3, day 7). Key data sources include:

1. **Single-cell data files**: Containing gene expression profiles for various cell types.
2. **Heatmap data files**: Summarizing gene expression averages across different conditions.

**Main steps of Data preprocessing:**

1. For each cell type, perform PCA to reduce dimensionality. Calculate the correlation of each principal component (PC) with the condition and time points. Select the two PCs that are most relevant to condition and time, minimizing individual differences, for use in PCA plots[1,2].

2. Identify the top 50 PC loadings for each cell type. Use these loadings to subset the gene expression profile, generating data for the heatmap (pseudo bulk level) and 1D scatter plot (single-cell level).

**Data Abstraction:** The data is abstracted into the following key elements:

- **Cell Types**: Different cell types, e.g., Monocyte_Classical, γδTCells.
- **Conditions**: Healthy, Mild, Severe.
- **Time Points**: Day 1, Day 3, Day 7.
- **Gene Expression**: Expression levels of various genes.

#### Task Abstraction

**High-Level Problem**: How can researchers effectively explore and analyze the complex single-cell RNA sequencing data from TBI patients to identify important genes and cellular behaviors under different conditions and time points?

**Low-Level Tasks**:

1. **T1**: Select and filter data by cell type.
2. **T2**: Adjust visual parameters (circle size, opacity) for better visibility.
3. **T3**: Examine general properties of cells via scatter plots.
4. **T4**: Interactively select specific conditions and time points within the scatter plot.
5. **T5**: Investigate gene expression levels using heatmaps.
6. **T6**: Select and explore specific genes using an autocomplete input.
7. **T7**: Use a brush tool to filter cells in the scatter plot and observe changes in gene expression over time.

#### Design Rationale

**Visual Representation and Interaction**:

- Scatter Plots (T1, T3, T4)[3]

  : Used to visualize the general properties of cells. Color coding represents different conditions, and selectors allow focusing on specific conditions and time points.

  - **Circle Size and Opacity Sliders (T2)**: Enable adjustments to improve plot readability and focus on specific data points.

- **Heatmap (T5)**: Displays averaged gene expression across conditions, helping identify trends and patterns in gene expression.

- **Autocomplete Input (T6)**: Facilitates the selection and analysis of specific genes, making the exploration of gene-level data more efficient.

- **Brush Tool (T7)**: Allows dynamic selection of cells within the scatter plot, updating the corresponding gene expression visualization to reflect the selected subset of data.

**Design Decisions**:

- **Color Encoding**: Conditions are encoded with distinct colors to allow easy differentiation between Healthy, Mild, and Severe conditions.
- **Interactive Filters**: Dropdown menus and sliders are used for filtering data by cell type and adjusting visualization parameters, providing a user-friendly interface.
- **Linked Views**: Scatter plots and heatmaps are linked, ensuring that selections in one view update the other, maintaining context and coherence.

#### Iterative Process

**Initial Concept**: The project began with an initial concept to visualize scRNA-seq data using static plots. Early feedback highlighted the need for interactivity to allow deeper exploration.

**First Iteration**:

- **Prototype Development**: An initial prototype with basic scatter plots and heatmaps.
- **User Feedback**: Received feedback on the lack of interactivity and difficulty in exploring specific genes and conditions.

**Second Iteration**:

- **Interactive Features**: Interactive widgets such as dropdowns, sliders, and autocomplete inputs.
- **Enhanced Visuals**: Improved scatter plot and heatmap designs, making them more informative and visually appealing.

**Final Iteration**:

- **Linking Views**: Implemented linked views between scatter plots and heatmaps.
- **Brush Tool**: Added the brush tool for dynamic selection and filtering of cells.
- **Polishing**: Refined UI elements and ensured smooth user interactions.

#### Lessons Learned

1. **Importance of Interactivity**: Interactive elements significantly enhance the user's ability to explore and understand complex datasets.
2. Linking different visualizations (scatter plots and heatmaps) provides a cohesive and comprehensive view of the data.
3. **Leveraging Brushing and Linked Selections in Vega**:
   - **Dynamic Updates with Brush Selection**: By using the brush selection tool in the Vega pane, users can dynamically select a region of interest in the scatter plot. This selection is then used to filter the data displayed in a linked table. This feature allows for real-time exploration of subsets of data, making the analysis process more interactive and insightful.
   - **Combining Brush and Autocomplete Input**: The final figure, which updates based on both the brush-selected region and the selected gene from the autocomplete input, showcased the powerful combination of interactive tools. By selecting a specific gene using the autocomplete input, users can focus on the expression levels of that gene. The brush tool further refines this view by allowing users to select specific cells or regions in the scatter plot[4], thereby updating the table and subsequent visualizations to reflect the gene expression within the selected subset. This dual-interaction mechanism provided a highly granular and focused exploration capability, demonstrating the utility of combining multiple interactive elements.
4. **Interactive Function for Showing Cell Properties**:
   - **Initial Attempt**: Initially, the goal was to display cell properties under different conditions and time points within the same scatter plot using color and shape as preattentive features. However, it was discovered that shape is a much weaker visual cue compared to color[5], making it difficult to clearly differentiate cells represented by shape.
   - **Refinement**: To address this, the approach was modified to use two linked scatter plots. This allowed for better visual distinction and interaction. By clicking to highlight selected conditions, users can more clearly see the distribution and properties of cells under different conditions and time points. This iterative change improved the usability and clarity of the visualization, demonstrating the importance of selecting appropriate visual encodings and the power of linked interactive plots.

#### References

1. Stuart, T., & Satija, R. (2019). Integrative single-cell analysis. Nature Reviews Genetics, 20(5), 257-272.
2. Macosko, E. Z., Basu, A., Satija, R., Nemesh, J., Shekhar, K., Goldman, M., ... & Regev, A. (2015). Highly parallel genome-wide expression profiling of individual cells using nanoliter droplets. Cell, 161(5), 1202-1214.
   
3. Han, X., Wang, R., Zhou, Y., Fei, L., Sun, H., Lai, S., ... & Guo, G. (2018). Mapping the Mouse Cell Atlas by Microwell-Seq. Cell, 172(5), 1091-1107.e17.
4. Wright, M. A., & Roberts, J. C. (2005). Click and brush: A novel way of finding correlations and relationships in visualizations. In *TPCG* (pp. 179-186).
5. Munzner, T. (2014). Visualization Analysis and Design. AK Peters/CRC Press.

----

[Link to video illustration](https://www.youtube.com/watch?v=ZCIpDxLSSdg&t=76s)

Link to Source code

Project Overview:
![image-20240516065317931](/Users/xiyuanzhang/Library/Application Support/typora-user-images/image-20240516065317931.png)