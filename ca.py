# coding=utf-8
# Created by Tuan Truong on 2018-03-09.
# © 2018 Framgia.
# v2.0.0

import sys
import os
from datetime import datetime
import subprocess
import re

#=================== Helpers ===================

def pasteboard_read():
	return subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def camelCase(st):
	output = ''.join(x for x in st.title() if x.isalpha())
	return output[0].lower() + output[1:]

#=================== BaseScene ===================

class SceneType:
	BASE = "--base"
	LIST = "--list"
	DETAIL = "--detail"

class BaseScene(object):
	def __init__(self, name, project, developer, company, date):
		super(BaseScene, self).__init__()
		self.name = name
		self.project = project
		self.developer = developer
		self.company = company
		self.date = date

	def _file_header(self, class_name):
		file_name = class_name + ".swift"
		header = "//\n"
		header += "// {}\n".format(file_name)
		header += "// {}\n".format(self.project)
		header += "//\n"
		header += "// Created by {} on {}.\n".format(self.developer, self.date)
		now = datetime.now()
		header += "// Copyright © {} {}. All rights reserved.\n".format(now.year, self.company)
		header += "//\n"
		header += "\n"
		return header

	def create_files(self):
		print(" ")
		self._make_dirs()
		self._create_view_model()
		self._create_navigator()
		self._create_use_case_type()
		self._create_use_case()
		self._create_view_controller()
		self._create_view_model_tests()
		self._create_use_case_mock()
		self._create_navigator_mock()
		self._create_view_controller_tests()
		print(" ")

	def _make_dirs(self):
		current_directory = os.getcwd()
		main_directory = os.path.join(current_directory, r'{}'.format(self.name))
		try: 
			os.makedirs(main_directory)
		except:
			pass
		else:
			test_directory = os.path.join(main_directory, "Test")
			try:
				os.makedirs(test_directory)
			except:
				pass

	def _create_view_model(self):
		class_name = self.name + "ViewModel"
		content = self._file_header(class_name)
		content += "struct {0}: ViewModelType {{\n\n".format(class_name)
		content += "    struct Input {\n\n    }\n\n"
		content += "    struct Output {\n\n    }\n\n"
		content += "    let navigator: {}NavigatorType\n".format(self.name)
		content += "    let useCase: {}UseCaseType\n\n".format(self.name)
		content += "    func transform(_ input: Input) -> Output {\n"
		content += "        return Output()\n"
		content += "    }\n"
		content += "}\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_navigator(self):
		class_name = self.name + "Navigator"
		protocol_name = class_name + "Type"
		content = self._file_header(class_name)
		content += "protocol {0} {{\n\n}}\n\n".format(protocol_name)
		content += "struct {}: {} {{\n\n}}\n".format(class_name, protocol_name)
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_use_case_type(self):
		class_name = self.name + "UseCaseType"
		content = self._file_header(class_name)
		content += "protocol {0} {{\n\n}}\n\n".format(class_name)
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_use_case(self):
		class_name = self.name + "UseCase"
		protocol_name = class_name + "Type"
		content = self._file_header(class_name)
		content += "struct {}: {} {{\n\n}}\n".format(class_name, protocol_name)
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_view_controller(self):
		class_name = self.name + "ViewController"
		content = self._file_header(class_name)
		content += "import UIKit\nimport Reusable\n\n"
		content += "final class {}: UIViewController, BindableType {{\n\n".format(class_name)
		content += "    var viewModel: {}ViewModel!\n\n".format(self.name)
		content += "    override func viewDidLoad() {\n"
		content += "        super.viewDidLoad()\n"
		content += "    }\n\n"
		content += "    deinit {\n"
		content += "        logDeinit()\n"
		content += "    }\n\n"
		content += "    func bindViewModel() {\n"
		content += "        let input = {}ViewModel.Input()\n".format(self.name)
		content += "        let output = viewModel.transform(input)\n"
		content += "    }\n\n}\n\n"
		content += "// MARK: - StoryboardSceneBased\n"
		content += "extension {}ViewController: StoryboardSceneBased {{\n".format(self.name)
		content += "    static var sceneStoryboard = UIStoryboard()\n"
		content += "}\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_view_model_tests(self):
		class_name = self.name + "ViewModelTests"
		content = self._file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import XCTest\nimport RxSwift\nimport RxBlocking\n\n"
		content += "final class {0}: XCTestCase {{\n\n".format(class_name)
		content += "    private var viewModel: {}ViewModel!\n".format(self.name)
		content += "    private var navigator: {}NavigatorMock!\n".format(self.name)
		content += "    private var useCase: {}UseCaseMock!\n".format(self.name)
		content += "    private var disposeBag: DisposeBag!\n\n"
		content += "    override func setUp() {\n"
		content += "        super.setUp()\n"
		content += "        navigator = {}NavigatorMock()\n".format(self.name)
		content += "        useCase = {}UseCaseMock()\n".format(self.name)
		content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase)\n".format(self.name)
		content += "        disposeBag = DisposeBag()\n"
		content += "    }\n\n"
		content += "    func test_triggerInvoked_() {\n"
		content += "        // arrange\n"
		content += "        let input = {}ViewModel.Input()\n".format(self.name)
		content += "        let output = viewModel.transform(input)\n\n"
		content += "        // act\n\n"
		content += "        // assert\n"
		content += "        XCTAssert(true)\n"
		content += "    }\n"
		content += "}\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_use_case_mock(self):
		class_name = self.name + "UseCaseMock"
		content = self._file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import RxSwift\n\n"
		content += "final class {0}: {1}UseCaseType {{\n\n}}\n".format(class_name, self.name)
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_navigator_mock(self):
		class_name = self.name + "NavigatorMock"
		content = self._file_header(class_name)
		content += "@testable import {}\n\n".format(self.project)
		content += "final class {0}: {1}NavigatorType {{\n\n}}\n".format(class_name, self.name)
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_view_controller_tests(self):
		class_name = self.name + "ViewControllerTests"
		content = self._file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import XCTest\nimport Reusable\n\n"
		content += "final class {0}: XCTestCase {{\n\n".format(class_name)
		content += "    var viewController: {}ViewController!\n\n".format(self.name)
		content += "    override func setUp() {\n"
		content += "        super.setUp()\n"
		content += "        viewController = {}ViewController.instantiate()\n".format(self.name)
		content += "    }\n\n"
		content += "    func test_ibOutlets() {\n"
		content += "        _ = viewController.view\n"
		content += "        XCTAssert(true)\n"
		content += "//      XCTAssertNotNil(viewController.tableView)\n"
		content += "    }\n"
		content += "}\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_file(self, file_path, file_name, content):
		with open(file_path, "w") as f:
			f.write(content)
			print("        new file:   {}".format(file_path))

#=================== ListScene ===================

class ListScene(BaseScene):

	def __init__(self, model, options, name, project, developer, company, date):
		super(ListScene, self).__init__(name, project, developer, company, date)
		self.model = model
		self.options = options

	@property
	def model_name(self):
		return self.model.name

	@property
	def model_variable(self):
		return camelCase(self.model_name)	

	def create_files(self):
		print(" ")
		self._make_dirs()
		self._create_view_model()
		self._create_navigator()
		self._create_use_case_type()
		self._create_use_case()
		self._create_view_controller()
		self._create_table_view_cell()
		self._create_view_model_tests()
		self._create_use_case_mock()
		self._create_navigator_mock()
		self._create_view_controller_tests()
		self._create_table_view_cell_tests()
		print(" ")

	def _create_file(self, file_path, file_name, content):
		with open(file_path, "w") as f:
			f.write(content)
			print("        new file:   {}".format(file_path))

	def _create_view_model(self):
		class_name = self.name + "ViewModel"
		content = self._file_header(class_name)
		content += "struct {0}: ViewModelType {{\n".format(class_name)
		content += "    struct Input {\n"
		content += "        let loadTrigger: Driver<Void>\n"
		content += "        let reloadTrigger: Driver<Void>\n"
		content += "        let loadMoreTrigger: Driver<Void>\n"
		content += "        let select{}Trigger: Driver<IndexPath>\n".format(self.model_name)
		content += "    }\n\n"
		content += "    struct Output {\n"
		content += "        let error: Driver<Error>\n"
		content += "        let loading: Driver<Bool>\n"
		content += "        let refreshing: Driver<Bool>\n"
		content += "        let loadingMore: Driver<Bool>\n"
		content += "        let fetchItems: Driver<Void>\n"
		content += "        let {}List: Driver<[{}]>\n".format(self.model_variable, self.model_name)
		content += "        let selected{}: Driver<Void>\n".format(self.model_name)
		content += "        let isEmptyData: Driver<Bool>\n"
		content += "    }\n\n"
		content += "    let navigator: {}NavigatorType\n".format(self.name)
		content += "    let useCase: {}UseCaseType\n\n".format(self.name)
		content += "    func transform(_ input: Input) -> Output {\n"
		content += "        let loadMoreOutput = setupLoadMorePaging(\n"
		content += "            loadTrigger: input.loadTrigger,\n"
		content += "            getItems: useCase.get{}List,\n".format(self.model_name)
		content += "            refreshTrigger: input.reloadTrigger,\n"
		content += "            refreshItems: useCase.get{}List,\n".format(self.model_name)
		content += "            loadmoreTrigger: input.loadMoreTrigger,\n"
		content += "            loadmoreItems: useCase.loadMore{}List)\n".format(self.model_name)
		content += "        let (page, fetchItems, loadError, loading, refreshing, loadingMore) = loadMoreOutput\n\n"
		content += "        let {}List = page\n".format(self.model_variable)
		content += "            .map { $0.items.map { $0 } }\n"
		content += "            .asDriverOnErrorJustComplete()\n\n"
		content += "        let selected{} = input.select{}Trigger\n".format(self.model_name, self.model_name)
		content += "            .withLatestFrom({}List) {{\n".format(self.model_variable)
		content += "                return ($0, $1)\n"
		content += "            }\n"
		content += "            .map {{ indexPath, {}List in\n".format(self.model_variable)
		content += "                return {}List[indexPath.row]\n".format(self.model_variable)
		content += "            }\n"
		content += "            .do(onNext: {{ {} in\n".format(self.model_variable)
		content += "                self.navigator.to{}Detail({}: {})".format(self.model_name, self.model_variable, self.model_variable)
		content += "            })\n"
		content += "            .mapToVoid()\n\n"
		content += "        let isEmptyData = Driver.combineLatest({}List, loading)\n".format(self.model_variable)
		content += "            .filter { !$0.1 }\n"
		content += "            .map { $0.0.isEmpty }\n\n"
		content += "        return Output(\n"
		content += "            error: loadError,\n"
		content += "            loading: loading,\n"
		content += "            refreshing: refreshing,\n"
		content += "            loadingMore: loadingMore,\n"
		content += "            fetchItems: fetchItems,\n"
		content += "            {}List: {}List,\n".format(self.model_variable, self.model_variable)
		content += "            selected{}: selected{},\n".format(self.model_name, self.model_name)
		content += "            isEmptyData: isEmptyData\n"
		content += "        )\n"
		content += "    }\n"
		content += "}\n\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_use_case_type(self):
		class_name = self.name + "UseCaseType"
		content = self._file_header(class_name)
		content += "protocol {0} {{\n".format(class_name)
		content += "    func get{}List() -> Observable<PagingInfo<{}>>\n".format(self.model_name, self.model_name)
		content += "    func loadMore{}List(page: Int) -> Observable<PagingInfo<{}>>\n".format(self.model_name, self.model_name)
		content += "}\n\n"

		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_use_case(self):
		class_name = self.name + "UseCase"
		protocol_name = class_name + "Type"
		content = self._file_header(class_name)
		content += "struct {}: {} {{\n".format(class_name, protocol_name)
		content += "    func get{}List() -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
		content += "        return loadMore{}List(page: 1)\n".format(self.model_name)
		content += "    }\n\n"
		content += "    func loadMore{}List(page: Int) -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
		content += "        return Observable.empty()\n"
		content += "    }\n"
		content += "}\n\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_navigator(self):
		class_name = self.name + "Navigator"
		protocol_name = class_name + "Type"
		content = self._file_header(class_name)
		content += "protocol {0} {{\n".format(protocol_name)
		content += "    func to{}()\n".format(self.name)
		content += "    func to{}Detail({}: {})\n".format(self.model_name, self.model_variable, self.model_name)
		content += "}\n\n"
		content += "struct {}: {} {{\n".format(class_name, protocol_name)
		content += "    unowned let navigationController: UINavigationController\n"
		content += "    let useCaseProvider: UseCaseProviderType\n\n"
		content += "    func to{}() {{\n".format(self.name)
		content += "//        let vc = {}ViewController.instantiate()\n".format(self.name)
		content += "//        let vm = {}ViewModel(navigator: self, useCase: useCaseProvider.make{}UseCase())\n".format(self.name, self.name)
		content += "//        vc.bindViewModel(to: vm)\n"
		content += "//        navigationController.pushViewController(vc, animated: true)\n"
		content += "    }\n\n"
		content += "    func to{}Detail({}: {}) {{\n\n".format(self.model_name, self.model_variable, self.model_name)
		content += "    }\n"
		content += "}\n\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_view_controller(self):
		class_name = self.name + "ViewController"
		content = self._file_header(class_name)
		content += "import UIKit\nimport Reusable\n\n"
		content += "final class {}: UIViewController, BindableType {{\n".format(class_name)
		content += "    @IBOutlet weak var tableView: LoadMoreTableView!\n"
		content += "    var viewModel: {}ViewModel!\n\n".format(self.name)
		content += "    override func viewDidLoad() {\n"
		content += "        super.viewDidLoad()\n"
		content += "        configView()\n"
		content += "    }\n\n"
		content += "    private func configView() {\n"
		content += "        tableView.do {\n"
		content += "            $0.loadMoreDelegate = self\n"
		content += "            $0.estimatedRowHeight = 550\n"
		content += "            $0.rowHeight = UITableViewAutomaticDimension\n"
		content += "            $0.register(cellType: {}Cell.self)\n".format(self.model_name)
		content += "            $0.fixContentInset()\n"
		content += "        }\n"
		content += "    }\n\n"
		content += "    override func viewDidLayoutSubviews() {\n"
		content += "        super.viewDidLayoutSubviews()\n"
		content += "        tableView.fixFooterFrame()\n"
		content += "    }\n\n"
		content += "    deinit {\n"
		content += "        logDeinit()\n"
		content += "    }\n\n"
		content += "    func bindViewModel() {\n"
		content += "        let input = {}ViewModel.Input(\n".format(self.name)
		content += "            loadTrigger: Driver.just(()),\n"
		content += "            reloadTrigger: tableView.refreshTrigger,\n"
		content += "            loadMoreTrigger: tableView.loadmoreTrigger,\n"
		content += "            select{}Trigger: tableView.rx.itemSelected.asDriver()\n".format(self.model_name)
		content += "        )\n"
		content += "        let output = viewModel.transform(input)\n"
		content += "        output.{}List\n".format(self.model_variable)
		content += "            .drive(tableView.rx.items) {{ tableView, index, {} in\n".format(self.model_variable)
		content += "                return tableView.dequeueReusableCell(\n"
		content += "                    for: IndexPath(row: index, section: 0),\n"
		content += "                    cellType: {}Cell.self)\n".format(self.model_name)
		content += "                    .then {\n"
		content += "                        $0.{} = {}\n".format(self.model_variable, self.model_variable)
		content += "                    }\n"
		content += "            }\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "        output.error\n"
		content += "            .drive(rx.error)\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "        output.loading\n"
		content += "            .drive(rx.isLoading)\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "        output.refreshing\n"
		content += "            .drive(tableView.refreshing)\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "        output.loadingMore\n"
		content += "            .drive(tableView.loadingMore)\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "        output.fetchItems\n"
		content += "            .drive()\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "        output.selected{}\n".format(self.model_name)
		content += "            .drive()\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "        output.isEmptyData\n"
		content += "            .drive()\n"
		content += "            .disposed(by: rx.disposeBag)\n"
		content += "    }\n\n}\n\n"
		content += "// MARK: - UITableViewDelegate\n"
		content += "extension {}ViewController: UITableViewDelegate {{\n".format(self.name)
		content += "    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {\n"
		content += "        tableView.deselectRow(at: indexPath, animated: true)\n"
		content += "    }\n"
		content += "}\n\n"
		content += "// MARK: - StoryboardSceneBased\n"
		content += "extension {}ViewController: StoryboardSceneBased {{\n".format(self.name)
		content += "    static var sceneStoryboard = UIStoryboard()\n}\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_table_view_cell(self):
		model = self.model
		class_name = self.model_name + "Cell"
		content = self._file_header(class_name)
		content += "import UIKit\n\n"
		content += "final class {}Cell: UITableViewCell, NibReusable {{\n".format(self.model_name)
		for p in model.properties:
			if p.name != "id":
				lowered_name = p.name.lower()
				if "image" in lowered_name or "url" in lowered_name:
					content += "    @IBOutlet weak var {}ImageView: UIImageView!\n".format(p.name)
				else:
					content += "    @IBOutlet weak var {}Label: UILabel!\n".format(p.name)
		content += "\n"
		content += "    var {}: {}? {{\n".format(self.model_variable, self.model_name)
		content += "        didSet {\n"
		content += "            guard let {} = {} else {{ return }}\n".format(self.model_variable, self.model_variable)
		for p in model.properties:
			if p.name != "id":
				lowered_name = p.name.lower()
				if "image" in lowered_name or "url" in lowered_name:
					content += "            {}ImageView.image = nil\n".format(p.name)
				else:
					content += '            {}Label.text = ""\n'.format(p.name)
		content += "        }\n"
		content += "    }\n\n"
		content += "    override func awakeFromNib() {\n"
		content += "        super.awakeFromNib()\n"
		content += "    }\n\n"
		content += "    override func prepareForReuse() {\n"
		content += "        super.prepareForReuse()\n"
		for p in model.properties:
			if p.name != "id":
				lowered_name = p.name.lower()
				if "image" in lowered_name or "url" in lowered_name:
					content += "        {}ImageView.image = nil\n".format(p.name)
				else:
					content += '        {}Label.text = ""\n'.format(p.name)
		content += "    }\n"
		content += "}\n\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_view_model_tests(self):
		class_name = self.name + "ViewModelTests"
		content = self._file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import XCTest\nimport RxSwift\nimport RxBlocking\n\n"
		content += "final class {}: XCTestCase {{\n".format(class_name)
		content += "    private var viewModel: {}ViewModel!\n".format(self.name)
		content += "    private var navigator: {}NavigatorMock!\n".format(self.name)
		content += "    private var useCase: {}UseCaseMock!\n".format(self.name)
		content += "    private var disposeBag: DisposeBag!\n"
		content += "    private var input: {}ViewModel.Input!\n".format(self.name)
		content += "    private var output: {}ViewModel.Output!\n".format(self.name)
		content += "    private var loadTrigger = PublishSubject<Void>()\n"
		content += "    private var reloadTrigger = PublishSubject<Void>()\n"
		content += "    private var loadMoreTrigger = PublishSubject<Void>()\n"
		content += "    private var select{}Trigger = PublishSubject<IndexPath>()\n\n".format(self.model_name)
		content += "    override func setUp() {\n"
		content += "        super.setUp()\n"
		content += "        navigator = {}NavigatorMock()\n".format(self.name)
		content += "        useCase = {}UseCaseMock()\n".format(self.name)
		content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase)\n".format(self.name)
		content += "        disposeBag = DisposeBag()\n"
		content += "        input = {}ViewModel.Input(\n".format(self.name)
		content += "            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),\n"
		content += "            reloadTrigger: reloadTrigger.asDriverOnErrorJustComplete(),\n"
		content += "            loadMoreTrigger: loadMoreTrigger.asDriverOnErrorJustComplete(),\n"
		content += "            select{}Trigger: select{}Trigger.asDriverOnErrorJustComplete()\n".format(self.model_name, self.model_name)
		content += "        )\n"
		content += "        output = viewModel.transform(input)\n"
		content += "        output.error.drive().disposed(by: disposeBag)\n"
		content += "        output.loading.drive().disposed(by: disposeBag)\n"
		content += "        output.refreshing.drive().disposed(by: disposeBag)\n"
		content += "        output.loadingMore.drive().disposed(by: disposeBag)\n"
		content += "        output.fetchItems.drive().disposed(by: disposeBag)\n"
		content += "        output.{}List.drive().disposed(by: disposeBag)\n".format(self.model_variable)
		content += "        output.selected{}.drive().disposed(by: disposeBag)\n".format(self.model_name)
		content += "        output.isEmptyData.drive().disposed(by: disposeBag)\n"
		content += "    }\n\n"
		content += "    func test_loadTriggerInvoked_get{}List() {{\n".format(self.model_name)
		content += "        // act\n"
		content += "        loadTrigger.onNext(())\n"
		content += "        let {}List = try? output.{}List.toBlocking(timeout: 1).first()\n".format(self.model_variable, self.model_variable)
		content += "        \n"
		content += "        // assert\n"
		content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
		content += "        XCTAssertEqual({}List??.count, 1)\n".format(self.model_variable)
		content += "    }\n\n"
		content += "    func test_loadTriggerInvoked_get{}List_failedShowError() {{\n".format(self.model_name)
		content += "        // arrange\n"
		content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        loadTrigger.onNext(())\n"
		content += "        get{}List_ReturnValue.onError(TestError())\n".format(self.model_name)
		content += "        let error = try? output.error.toBlocking(timeout: 1).first()\n\n"
		content += "        // assert\n"
		content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
		content += "        XCTAssert(error is TestError)\n"
		content += "    }\n\n"
		content += "    func test_reloadTriggerInvoked_get{}List() {{\n".format(self.model_name)
		content += "        // act\n"
		content += "        reloadTrigger.onNext(())\n"
		content += "        let {}List = try? output.{}List.toBlocking(timeout: 1).first()\n\n".format(self.model_variable, self.model_variable)
		content += "        // assert\n"
		content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
		content += "        XCTAssertEqual({}List??.count, 1)\n".format(self.model_variable)
		content += "    }\n\n"
		content += "    func test_reloadTriggerInvoked_get{}List_failedShowError() {{\n".format(self.model_name)
		content += "        // arrange\n"
		content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        reloadTrigger.onNext(())\n"
		content += "        get{}List_ReturnValue.onError(TestError())\n".format(self.model_name)
		content += "        let error = try? output.error.toBlocking(timeout: 1).first()\n\n"
		content += "        // assert\n"
		content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
		content += "        XCTAssert(error is TestError)\n"
		content += "    }\n\n"
		content += "    func test_reloadTriggerInvoked_notGet{}ListIfStillLoading() {{\n".format(self.model_name)
		content += "        // arrange\n"
		content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        loadTrigger.onNext(())\n"
		content += "        useCase.get{}List_Called = false\n".format(self.model_name)
		content += "        reloadTrigger.onNext(())\n\n"
		content += "        // assert\n"
		content += "        XCTAssertFalse(useCase.get{}List_Called)\n".format(self.model_name)
		content += "    }\n\n"
		content += "    func test_reloadTriggerInvoked_notGet{}ListIfStillReloading() {{\n".format(self.model_name)
		content += "        // arrange\n"
		content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        reloadTrigger.onNext(())\n"
		content += "        useCase.get{}List_Called = false\n".format(self.model_name)
		content += "        reloadTrigger.onNext(())\n\n"
		content += "        // assert\n"
		content += "        XCTAssertFalse(useCase.get{}List_Called)\n".format(self.model_name)
		content += "    }\n\n"
		content += "    func test_loadMoreTriggerInvoked_loadMore{}List() {{\n".format(self.model_name)
		content += "        // act\n"
		content += "        loadTrigger.onNext(())\n"
		content += "        loadMoreTrigger.onNext(())\n"
		content += "        let {}List = try? output.{}List.toBlocking(timeout: 1).first()\n\n".format(self.model_variable, self.model_variable)
		content += "        // assert\n"
		content += "        XCTAssert(useCase.loadMore{}List_Called)\n".format(self.model_name)
		content += "        XCTAssertEqual({}List??.count, 2)\n".format(self.model_variable)
		content += "    }\n\n"
		content += "    func test_loadMoreTriggerInvoked_loadMore{}List_failedShowError() {{\n".format(self.model_name)
		content += "        // arrange\n"
		content += "        let loadMore{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.loadMore{}List_ReturnValue = loadMore{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        loadTrigger.onNext(())\n"
		content += "        loadMoreTrigger.onNext(())\n"
		content += "        loadMore{}List_ReturnValue.onError(TestError())\n".format(self.model_name)
		content += "        let error = try? output.error.toBlocking(timeout: 1).first()\n\n"
		content += "        // assert\n"
		content += "        XCTAssert(useCase.loadMore{}List_Called)\n".format(self.model_name)
		content += "        XCTAssert(error is TestError)\n"
		content += "    }\n\n"
		content += "    func test_loadMoreTriggerInvoked_notLoadMore{}ListIfStillLoading() {{\n".format(self.model_name)
		content += "        // arrange\n"
		content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        loadTrigger.onNext(())\n"
		content += "        useCase.get{}List_Called = false\n".format(self.model_name)
		content += "        loadMoreTrigger.onNext(())\n\n"
		content += "        // assert\n"
		content += "        XCTAssertFalse(useCase.loadMore{}List_Called)\n".format(self.model_name)
		content += "    }\n\n"
		content += "    func test_loadMoreTriggerInvoked_notLoadMore{}ListIfStillReloading() {{\n".format(self.model_name)
		content += "        // arrange\n"
		content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        reloadTrigger.onNext(())\n"
		content += "        useCase.get{}List_Called = false\n".format(self.model_name)
		content += "        loadMoreTrigger.onNext(())\n"
		content += "        // assert\n"
		content += "        XCTAssertFalse(useCase.loadMore{}List_Called)\n".format(self.model_name)
		content += "    }\n\n"
		content += "    func test_loadMoreTriggerInvoked_notLoadMoreDocumentTypesStillLoadingMore() {\n"
		content += "        // arrange\n"
		content += "        let loadMore{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
		content += "        useCase.loadMore{}List_ReturnValue = loadMore{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        loadMoreTrigger.onNext(())\n"
		content += "        useCase.loadMore{}List_Called = false\n".format(self.model_name)
		content += "        loadMoreTrigger.onNext(())\n\n"
		content += "        // assert\n"
		content += "        XCTAssertFalse(useCase.loadMore{}List_Called)\n".format(self.model_name)
		content += "    }\n\n"
		content += "    func test_select{}TriggerInvoked_to{}Detail() {{\n".format(self.model_name, self.model_name)
		content += "        // act\n"
		content += "        loadTrigger.onNext(())\n"
		content += "        select{}Trigger.onNext(IndexPath(row: 0, section: 0))\n\n".format(self.model_name)
		content += "        // assert\n"
		content += "        XCTAssert(navigator.to{}Detail_Called)\n".format(self.model_name)
		content += "    }\n"
		content += "}\n\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_use_case_mock(self):
		class_name = self.name + "UseCaseMock"
		content = self._file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import RxSwift\n\n"
		content += "final class {0}: {1}UseCaseType {{\n\n".format(class_name, self.name)
		content += "    // MARK: - get{}List\n".format(self.model_name)
		content += "    var get{}List_Called = false\n".format(self.model_name)
		content += "    var get{}List_ReturnValue: Observable<PagingInfo<{}>> = {{\n".format(self.model_name, self.model_name)
		content += "        let items = [\n"
		content += "            {}(builder: {}Builder().then {{\n".format(self.model_name, self.model_name)
		content += "                $0.id = 1\n"
		content += "            })\n"
		content += "        ]\n"
		content += "        let page = PagingInfo<{}>(page: 1, items: OrderedSet(sequence: items))\n".format(self.model_name)
		content += "        return Observable.just(page)\n"
		content += "    }()\n"
		content += "    func get{}List() -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
		content += "        get{}List_Called = true\n".format(self.model_name)
		content += "        return get{}List_ReturnValue\n".format(self.model_name)
		content += "    }\n\n"
		content += "    // MARK: - loadMore{}List\n".format(self.model_name)
		content += "    var loadMore{}List_Called = false\n".format(self.model_name)
		content += "    var loadMore{}List_ReturnValue: Observable<PagingInfo<{}>> = {{\n".format(self.model_name, self.model_name)
		content += "        let items = [\n"
		content += "            {}(builder: {}Builder().then {{\n".format(self.model_name, self.model_name)
		content += "                $0.id = 2\n"
		content += "            })\n"
		content += "        ]\n"
		content += "        let page = PagingInfo<{}>(page: 2, items: OrderedSet(sequence: items))\n".format(self.model_name)
		content += "        return Observable.just(page)\n"
		content += "    }()\n"

		content += "    func loadMore{}List(page: Int) -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
		content += "        loadMore{}List_Called = true\n".format(self.model_name)
		content += "        return loadMore{}List_ReturnValue\n".format(self.model_name)
		content += "    }\n"
		content += "}\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_navigator_mock(self):
		class_name = self.name + "NavigatorMock"
		content = self._file_header(class_name)
		content += "@testable import {}\n\n".format(self.project)
		content += "final class {0}: {1}NavigatorType {{\n\n".format(class_name, self.name)
		content += "    // MARK: - to{}\n".format(self.name)
		content += "    var to{}_Called = false\n".format(self.name)
		content += "    func to{}() {{\n".format(self.name)
		content += "        to{}_Called = true\n".format(self.name)
		content += "    }\n\n"
		content += "    // MARK: - to{}Detail\n".format(self.model_name)
		content += "    var to{}Detail_Called = false\n".format(self.model_name)
		content += "    func to{}Detail({}: {}) {{\n".format(self.model_name, self.model_variable, self.model_name)
		content += "        to{}Detail_Called = true\n".format(self.model_name)
		content += "    }\n"
		content += "}\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_view_controller_tests(self):
		class_name = self.name + "ViewControllerTests"
		content = self._file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import XCTest\nimport Reusable\n\n"
		content += "final class {0}: XCTestCase {{\n\n".format(class_name)
		content += "    private var viewController: {}ViewController!\n\n".format(self.name)
		content += "    override func setUp() {\n		super.setUp()\n"
		content += "//        viewController = {}ViewController.instantiate()\n	}}\n\n".format(self.name)
		content += "    func test_ibOutlets() {\n"
		content += "//        _ = viewController.view\n"
		content += "//        XCTAssertNotNil(viewController.tableView)\n"
		content += "    }\n}\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

	def _create_table_view_cell_tests(self):
		class_name = self.name + "{}CellTests".format(self.model_name)
		content = self._file_header(class_name)
		content += "import XCTest\n"
		content += "@testable import {}\n\n".format(self.project)
		content += "final class {}CellTests: XCTestCase {{\n".format(self.model_name)
		content += "    var cell: {}Cell!\n\n".format(self.model_name)
		content += "    override func setUp() {\n"
		content += "        super.setUp()\n"
		content += "//        cell = {}Cell.loadFromNib()\n".format(self.model_name)
		content += "    }\n\n"
		content += "    func test_iboutlets() {\n"
		content += "//        XCTAssertNotNil(cell)\n"
		for p in self.model.properties:
			if p.name != "id":
				lowered_name = p.name.lower()
				if "image" in lowered_name or "url" in lowered_name:
					content += "//        XCTAssertNotNil(cell.{}ImageView)\n".format(p.name)
				else:
					content += "//        XCTAssertNotNil(cell.{}Label)\n".format(p.name)
		content += "    }\n"
		content += "}\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self._create_file(file_path, file_name, content)

#=================== Support Class ===================

class Model(object):
	def __init__(self, name, properties):
		super(Model, self).__init__()
		self.name = name
		self.properties = properties
		self.test = "1213"


class Property(object):
	def __init__(self, property):
		super(Property, self).__init__()
		self.property = property
		property_regex = re.compile("(?:let|var) (\w+): (.*)")
		mo = property_regex.search(property)
		self.name = mo.group(1)
		self.type = PropertyType(mo.group(2))


class PropertyType(object):
	def __init__(self, type):
		super(PropertyType, self).__init__()
		self.type = type

	def isOptional(self):
		return self.type.endswith("?")

	def isArray(self):
		return self.type.endswith("]") or self.type.endswith("]?")


#=================== Main ===================

	
# model_text = """
# struct Conversation {
# 	let id: Int
# 	let name: String
# 	let profileImageURLString: String?
# 	let firstLogin: Bool
# 	let birthday: Date
# 	let jskStatus: [Bool]?
# }
# """

# model = parse_model(model_text)

# args = [SceneType.LIST]
# options = args[1:]
# scene = ListScene(model, options, "Messages", "iTool", "Tuan Truong", "Framgia", "2018-05-20")
# scene.create_files()

def parse_model(model_text):
	model_regex = re.compile("(?:struct|class) (\w+) {([^}]+)")
	match = model_regex.search(model_text)
	model_name = match.group(1)
	property_block = match.group(2)
	property_regex = re.compile("(?:let|var) (\w+): (.*)")
	properties = [Property(p.group()) for p in property_regex.finditer(property_block)]
	return Model(model_name, properties)

def create_files(args):
	now = datetime.now()
	date = "{}/{}/{}".format(now.month, now.day, now.strftime("%y"))
	file_name = "ca_info.txt"
	try:
		with open(file_name) as f:
			content = f.readlines()
			info = [x.strip() for x in content]
			project = info[0]
			developer = info[1]
			company = info[2]
	except:
		project = raw_input('Enter project name: ')
		developer = raw_input('Enter developer name: ')
		company = raw_input('Enter company name: ')
		content = "\n".join([project, developer, company])
		with open(file_name, "w") as f:	
			f.write(content)
	name = args[0]
	if len(args) == 1:
		scene = BaseScene(name, project, developer, company, date)
		scene.create_files()
		print("Finish!")
	elif len(args) > 1:
		scene_type = args[1]
		options = args[2:]
		if scene_type == SceneType.LIST:
			model_text = pasteboard_read()
			try:
				model = parse_model(model_text)
				scene = ListScene(model, options, name, project, developer, company, date)
				scene.create_files()
				print("Finish!")
			except:
				print('Invalid model text in clipboard.')
		else:
			print("Invalid params.")
	

if len(sys.argv) > 1:
	create_files(sys.argv[1:])
else:
	print('Please enter a scene name.')

		
