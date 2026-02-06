import SwiftUI

/// Home screen showing featured courses and categories.
struct HomeView: View {
    @ObservedObject var viewModel: HomeViewModel
    var onCourseSelected: (Course) -> Void
    var onCategorySelected: (Category) -> Void

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    // Featured Courses
                    if !viewModel.featuredCourses.isEmpty {
                        SectionHeader(title: "Featured Courses")

                        ScrollView(.horizontal, showsIndicators: false) {
                            LazyHStack(spacing: 16) {
                                ForEach(viewModel.featuredCourses) { course in
                                    CourseCard(course: course)
                                        .onTapGesture { onCourseSelected(course) }
                                }
                            }
                            .padding(.horizontal)
                        }
                    }

                    // Categories
                    if !viewModel.categories.isEmpty {
                        SectionHeader(title: "Categories")

                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: 16) {
                            ForEach(viewModel.categories) { category in
                                CategoryCard(category: category)
                                    .onTapGesture { onCategorySelected(category) }
                            }
                        }
                        .padding(.horizontal)
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("EduPath")
            .refreshable {
                await viewModel.loadData()
            }
            .overlay {
                if viewModel.isLoading && viewModel.featuredCourses.isEmpty {
                    ProgressView()
                }
            }
        }
        .task {
            await viewModel.loadData()
        }
    }
}

/// Section header with title.
struct SectionHeader: View {
    let title: String

    var body: some View {
        Text(title)
            .font(.title2)
            .fontWeight(.bold)
            .padding(.horizontal)
    }
}
