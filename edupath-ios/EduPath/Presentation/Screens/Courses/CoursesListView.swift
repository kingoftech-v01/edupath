import SwiftUI

/// Courses list with search and category filter.
struct CoursesListView: View {
    @ObservedObject var viewModel: CoursesViewModel
    var onCourseSelected: (Course) -> Void

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Search bar
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.secondary)

                    TextField("Search courses...", text: $viewModel.searchQuery)
                        .textFieldStyle(.plain)
                        .onSubmit { viewModel.search() }

                    if !viewModel.searchQuery.isEmpty {
                        Button(action: {
                            viewModel.searchQuery = ""
                            viewModel.search()
                        }) {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .padding()
                .background(Color.gray.opacity(0.1))

                // Filter chips
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        FilterChip(
                            title: "Free",
                            isSelected: viewModel.showFreeOnly
                        ) {
                            viewModel.toggleFreeOnly()
                        }

                        ForEach(viewModel.categories) { category in
                            FilterChip(
                                title: category.name,
                                isSelected: viewModel.selectedCategory?.id == category.id
                            ) {
                                viewModel.selectCategory(
                                    viewModel.selectedCategory?.id == category.id ? nil : category
                                )
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 8)
                }

                // Course list
                if viewModel.isLoading && viewModel.courses.isEmpty {
                    Spacer()
                    ProgressView()
                    Spacer()
                } else if viewModel.courses.isEmpty {
                    Spacer()
                    Text("No courses found")
                        .foregroundColor(.secondary)
                    Spacer()
                } else {
                    List(viewModel.courses) { course in
                        CourseRow(course: course)
                            .onTapGesture { onCourseSelected(course) }
                    }
                    .listStyle(.plain)
                }
            }
            .navigationTitle("Courses")
        }
        .task {
            await viewModel.loadCategories()
            await viewModel.loadCourses()
        }
    }
}

/// Single course row in list.
struct CourseRow: View {
    let course: Course

    var body: some View {
        HStack(spacing: 12) {
            AsyncImage(url: course.imageURL) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Rectangle()
                    .fill(Color.gray.opacity(0.2))
            }
            .frame(width: 80, height: 60)
            .clipShape(RoundedRectangle(cornerRadius: 8))

            VStack(alignment: .leading, spacing: 4) {
                Text(course.title)
                    .font(.headline)
                    .lineLimit(2)

                if let instructor = course.instructor {
                    Text(instructor.name)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Text(course.formattedPrice)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                    .foregroundColor(course.isFree ? .green : .primary)
            }
        }
        .padding(.vertical, 4)
    }
}

/// Filter chip button.
struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(isSelected ? Color.accentColor : Color.gray.opacity(0.2))
                .foregroundColor(isSelected ? .white : .primary)
                .cornerRadius(16)
        }
    }
}
